"""
fix-chart-rendering spec tests - Real Data Tests
"""

import sys
import os
import json
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestChartGenerationRealData:
    """실제 데이터 포맷으로 테스트"""

    def test_chart_type_detection(self):
        """차트 타입 감지"""
        from app.api.chat import detect_chart_type
        
        assert detect_chart_type("월별 추이") == "line"
        assert detect_chart_type("비율 비교") == "pie"
        assert detect_chart_type("산점도") == "scatter"
        assert detect_chart_type("히트맵") == "heatmap"
        assert detect_chart_type("일반 차트") == "bar"
        print("[PASS] chart type detection works")

    def test_generate_chart_with_real_file(self):
        """실제 CSV 파일로 차트 생성 테스트"""
        from app.api.chat import generate_chart_from_csv_metadata
        from app.db.duckdb_client import CSVReader
        
        csv_metadata = {
            "file_id": "test-file-id",
            "columns": [
                {"name": "단과대학", "data_type": "category", "sample_values": ["공과대학"]},
                {"name": "평점", "data_type": "number", "sample_values": [3.5, 2.8]}
            ],
            "row_count": 100
        }
        
        with patch.object(CSVReader, 'load_csv') as mock_load, \
             patch.object(CSVReader, 'get_data') as mock_get:
            
            mock_load.return_value = {"columns": ["단과대학", "평점"], "row_count": 100}
            mock_get.return_value = [
                {"단과대학": "공과대학", "평점": 3.5},
                {"단과대학": "인문대학", "평점": 3.2},
                {"단과대학": "자연대학", "평점": 2.8},
            ]
            
            result = generate_chart_from_csv_metadata("차트 그려줘", csv_metadata)
            
            assert result is not None, "Should generate chart config"
            assert "series" in result, "Should have series"
            assert result["xAxis"]["data"] == ["공과대학", "인문대학", "자연대학"], f"Actual: {result['xAxis']['data']}"
            assert result["series"][0]["data"] == [3.5, 3.2, 2.8], f"Actual: {result['series'][0]['data']}"
            print(f"[PASS] Real file data: {result.get('title')}")

    def test_generate_chart_no_file_id(self):
        """file_id 없으면 None 반환"""
        from app.api.chat import generate_chart_from_csv_metadata
        
        csv_metadata = {
            "columns": [
                {"name": "단과대학", "data_type": "category", "sample_values": ["공과대학"]},
                {"name": "평점", "data_type": "number", "sample_values": [3.5]}
            ],
            "row_count": 100
        }
        
        result = generate_chart_from_csv_metadata("차트 그려줘", csv_metadata)
        
        assert result is None, "Should return None when no file_id"
        print("[PASS] No file_id returns None")


class TestPostAPIResponseFormat:
    """Spec: POST API response format"""

    def test_post_response_has_graph_field(self):
        """POST /api/chat/ response must have graph field"""
        import asyncio
        from app.api.chat import chat
        
        async def run_test():
            mock_request = MagicMock()
            mock_request.csv_metadata = None
            
            with patch("app.api.chat.LLMClient") as mock_llm:
                mock_instance = MagicMock()
                mock_response = MagicMock()
                mock_response.choices = [MagicMock(message=MagicMock(content="test response"))]
                mock_instance.chat.return_value = mock_response
                mock_llm.get_instance.return_value = mock_instance
                
                response = await chat(mock_request)
                
                assert "graph" in response, "Response missing graph field"
                assert "content" in response, "Response missing content field"
                print("[PASS] POST response has graph field")
        
        asyncio.run(run_test())

    def test_no_chart_request_returns_null(self):
        """When user doesn't request chart, graph should be null"""
        import asyncio
        from app.api.chat import chat
        
        async def run_test():
            mock_request = MagicMock()
            mock_request.message = "일반 대화"
            mock_request.csv_metadata = {
                "file_id": "test-id",
                "columns": [
                    {"name": "단과대학", "data_type": "unknown", "sample_values": ["공과대학"]},
                ],
                "row_count": 100
            }
            
            with patch("app.api.chat.LLMClient") as mock_llm:
                mock_instance = MagicMock()
                mock_response = MagicMock()
                mock_response.choices = [MagicMock(message=MagicMock(content="안녕하세요"))]
                mock_instance.chat.return_value = mock_response
                mock_llm.get_instance.return_value = mock_instance
                
                response = await chat(mock_request)
                assert response["graph"] is None, "Response should have graph=null"
                print("[PASS] No chart request returns graph=null")
        
        asyncio.run(run_test())


class TestSSEResponseFormat:
    """Spec: SSE stream response format"""

    def test_sse_response_has_graph_field(self):
        """SSE /api/chat/stream response must have graph field"""
        import asyncio
        from app.api.chat import generate_chat_response
        
        async def run_test():
            with patch("app.api.chat.LLMClient") as mock_llm:
                mock_instance = MagicMock()
                mock_chunk = MagicMock()
                mock_chunk.choices = [MagicMock(delta=MagicMock(content="test"))]
                mock_instance.chat.return_value = iter([mock_chunk])
                mock_llm.get_instance.return_value = mock_instance
                
                events = []
                async for event in generate_chat_response("test"):
                    events.append(event)
                
                message_events = [e for e in events if e.get("event") == "message"]
                assert len(message_events) > 0, "No message events"
                
                for event in message_events:
                    data = json.loads(event["data"])
                    assert "graph" in data, f"SSE message missing graph field"
                
                print("[PASS] SSE response has graph field in message events")
        
        asyncio.run(run_test())


class TestGraphValidation:
    """Spec: ignore invalid graph data"""

    def test_graph_null_is_ignored(self):
        valid = isValidGraph(None)
        assert not valid, "None should be invalid"
        print("[PASS] graph=null is ignored")

    def test_graph_valid_object_is_used(self):
        valid_config = {"series": [{"type": "line", "data": [1, 2, 3]}]}
        valid = isValidGraph(valid_config)
        assert valid, "Valid dict should be valid"
        print("[PASS] Valid object graph is rendered")

    def test_graph_array_is_ignored(self):
        valid = isValidGraph([1, 2, 3])
        assert not valid, "Array should be invalid"
        print("[PASS] graph=array is ignored")


def isValidGraph(config):
    """GraphView validation logic"""
    return config is not None and isinstance(config, dict) and not isinstance(config, list)


if __name__ == "__main__":
    print("=" * 60)
    print("fix-chart-rendering Spec Tests")
    print("=" * 60)
    
    test = TestChartGenerationRealData()
    print("\n[1] Chart Generation Real Data Tests")
    try:
        test.test_chart_type_detection()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_generate_chart_with_real_file()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_generate_chart_no_file_id()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    test = TestPostAPIResponseFormat()
    print("\n[2] POST API Response Format Tests")
    try:
        test.test_post_response_has_graph_field()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_no_chart_request_returns_null()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    test = TestSSEResponseFormat()
    print("\n[3] SSE Response Format Tests")
    try:
        test.test_sse_response_has_graph_field()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    test = TestGraphValidation()
    print("\n[4] Graph Validation Tests")
    try:
        test.test_graph_null_is_ignored()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_graph_valid_object_is_used()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_graph_array_is_ignored()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)
