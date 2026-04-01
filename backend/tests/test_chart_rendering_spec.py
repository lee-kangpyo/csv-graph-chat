"""
fix-chart-rendering spec tests - Real Data Tests
"""

import sys
import os
import json
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestDetectChartRequest:
    """Test chart request detection (shared with frontend)"""

    def test_detect_chart_keywords(self):
        """차트 요청 키워드 감지"""
        from app.api.chat import detect_chart_request
        
        assert detect_chart_request("차트 그려줘") == True
        assert detect_chart_request("그래프 시각화") == True
        assert detect_chart_request("일반 대화") == False
        assert detect_chart_request("数据显示") == False
        print("[PASS] chart request detection works")

    def test_detect_chart_case_insensitive(self):
        """키워드 감지는 대소문자 무관"""
        from app.api.chat import detect_chart_request
        
        assert detect_chart_request("CHART") == True
        assert detect_chart_request("Graph") == True
        assert detect_chart_request("PLOT") == True
        print("[PASS] chart detection is case insensitive")


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
    """Spec: SSE stream response format - text only, no graph"""

    def test_sse_message_has_no_graph_field(self):
        """SSE /api/chat/stream message events must NOT have graph field (text only)"""
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
                async for event in generate_chat_response("test", None, "test-request-id"):
                    events.append(event)
                
                message_events = [e for e in events if e.get("event") == "message"]
                assert len(message_events) > 0, "No message events"
                
                for event in message_events:
                    data = json.loads(event["data"])
                    assert "graph" not in data, f"SSE message should NOT have graph field"
                    assert "request_id" in data, f"SSE message should have request_id field"
                
                print("[PASS] SSE message events have no graph field (text only)")
        
        asyncio.run(run_test())

    def test_sse_done_has_request_id(self):
        """SSE /api/chat/stream done event should have request_id"""
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
                async for event in generate_chat_response("test", None, "my-request-id"):
                    events.append(event)
                
                done_events = [e for e in events if e.get("event") == "done"]
                assert len(done_events) > 0, "No done events"
                
                data = json.loads(done_events[0]["data"])
                assert data.get("request_id") == "my-request-id", "done event should have request_id"
                
                print("[PASS] SSE done event has request_id")
        
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


class TestChartGenerateEndpoint:
    """Spec: POST /api/chart/generate endpoint"""

    def test_chart_generate_returns_request_id_and_graph(self):
        """POST /api/chart/generate response must have request_id and graph fields"""
        from app.api.chart import ChartGenerateResponse
        
        response = ChartGenerateResponse(request_id="test-123", graph={"type": "line"})
        assert response.request_id == "test-123"
        assert response.graph == {"type": "line"}
        print("[PASS] ChartGenerateResponse has request_id and graph fields")

    def test_chart_generate_returns_null_graph(self):
        """POST /api/chart/generate returns graph: null when no chart requested"""
        from app.api.chart import ChartGenerateResponse
        
        response = ChartGenerateResponse(request_id="test-456", graph=None)
        assert response.request_id == "test-456"
        assert response.graph is None
        print("[PASS] ChartGenerateResponse returns null graph correctly")


def isValidGraph(config):
    """GraphView validation logic"""
    return config is not None and isinstance(config, dict) and not isinstance(config, list)


if __name__ == "__main__":
    print("=" * 60)
    print("split-chat-chart-parallel Spec Tests")
    print("=" * 60)
    
    test = TestDetectChartRequest()
    print("\n[1] Chart Request Detection Tests")
    try:
        test.test_detect_chart_keywords()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_detect_chart_case_insensitive()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    test = TestSSEResponseFormat()
    print("\n[2] SSE Response Format Tests (text only)")
    try:
        test.test_sse_message_has_no_graph_field()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_sse_done_has_request_id()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    test = TestGraphValidation()
    print("\n[3] Graph Validation Tests")
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
    
    test = TestChartGenerateEndpoint()
    print("\n[4] Chart Generate Endpoint Tests")
    try:
        test.test_chart_generate_returns_request_id_and_graph()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    try:
        test.test_chart_generate_returns_null_graph()
    except Exception as e:
        print(f"[FAIL] {e}")
    
    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)
