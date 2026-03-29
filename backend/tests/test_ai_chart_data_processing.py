"""
ai-chart-data-processing tests - LLM Intent & Pandas Processing Tests
"""

import sys
import os
import json
import tempfile
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestAnalysisIntentParsing:
    """LLM 응답에서 분석 intent 파싱 테스트"""

    def test_parse_valid_group_by_intent(self):
        """유효한 group_by intent JSON 파싱"""
        from app.api.insight_recommendation import parse_analysis_intent

        response = '{"analysis_type": "group_by", "group_by": "학과", "value": "평점", "agg_func": "mean", "chart_type": "bar"}'
        result = parse_analysis_intent(response)

        assert result is not None
        assert result["analysis_type"] == "group_by"
        assert result["group_by"] == "학과"
        assert result["value"] == "평점"
        assert result["agg_func"] == "mean"
        assert result["chart_type"] == "bar"
        print("[PASS] Valid group_by intent parsed")

    def test_parse_valid_time_series_intent(self):
        """유효한 time_series intent JSON 파싱"""
        from app.api.insight_recommendation import parse_analysis_intent

        response = '{"analysis_type": "time_series", "time_col": "날짜", "value": "매출", "freq": "monthly", "chart_type": "line"}'
        result = parse_analysis_intent(response)

        assert result is not None
        assert result["analysis_type"] == "time_series"
        assert result["time_col"] == "날짜"
        assert result["value"] == "매출"
        assert result["freq"] == "monthly"
        print("[PASS] Valid time_series intent parsed")

    def test_parse_intent_with_surrounding_text(self):
        """주변 텍스트가 포함된 JSON 파싱"""
        from app.api.insight_recommendation import parse_analysis_intent

        response = '''분석 결과를 다음과 같이 제안합니다.
{"analysis_type": "group_by", "group_by": "지역", "value": "매출", "agg_func": "sum", "chart_type": "pie"}
以上就是 제 제안입니다.'''
        result = parse_analysis_intent(response)

        assert result is not None
        assert result["analysis_type"] == "group_by"
        assert result["group_by"] == "지역"
        print("[PASS] Intent parsed from surrounding text")

    def test_parse_invalid_json_returns_none(self):
        """유효하지 않은 JSON 시 None 반환"""
        from app.api.insight_recommendation import parse_analysis_intent

        response = "This is not a JSON response"
        result = parse_analysis_intent(response)

        assert result is None
        print("[PASS] Invalid JSON returns None")

    def test_parse_missing_analysis_type_returns_none(self):
        """analysis_type 없는 JSON 시 None 반환"""
        from app.api.insight_recommendation import parse_analysis_intent

        response = '{"group_by": "학과", "value": "평점"}'
        result = parse_analysis_intent(response)

        assert result is None
        print("[PASS] Missing analysis_type returns None")


class TestFallbackIntent:
    """파싱 실패 시 fallback 로직 테스트"""

    def test_fallback_with_category_and_number_columns(self):
        """카테고리 + 숫자 컬럼이 있을 때 fallback 생성"""
        from app.api.insight_recommendation import get_fallback_intent

        columns = [
            {"name": "학과", "data_type": "category"},
            {"name": "평점", "data_type": "number"},
        ]
        result = get_fallback_intent(columns)

        assert result is not None
        assert result["analysis_type"] == "group_by"
        assert result["group_by"] == "학과"
        assert result["value"] == "평점"
        assert result["agg_func"] == "mean"
        print("[PASS] Fallback intent created")

    def test_fallback_with_time_series_keywords(self):
        """시계열 요청 키워드 시 line 차트"""
        from app.api.insight_recommendation import get_fallback_intent

        columns = [
            {"name": "학과", "data_type": "category"},
            {"name": "평점", "data_type": "number"},
        ]
        result = get_fallback_intent(columns, "월별 추이")

        assert result["chart_type"] == "line"
        print("[PASS] Fallback with time series keyword")

    def test_fallback_no_number_columns_returns_none(self):
        """숫자 컬럼이 없으면 None 반환"""
        from app.api.insight_recommendation import get_fallback_intent

        columns = [
            {"name": "학과", "data_type": "category"},
        ]
        result = get_fallback_intent(columns)

        assert result is None
        print("[PASS] Fallback returns None when no number columns")


class TestPandasProcessing:
    """pandas 데이터 처리 테스트"""

    def setup_test_csv(self):
        """테스트용 CSV 파일 생성"""
        content = """학과,평점,학생수
공과대학,3.5,100
인문대학,3.2,80
자연대학,2.8,60
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            return f.name

    def test_process_group_by_mean(self):
        """group_by mean 처리"""
        from app.api.pandas_processor import process_group_by

        csv_path = self.setup_test_csv()
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)

            labels, values = process_group_by(df, "학과", "평점", "mean")

            assert labels == ["공과대학", "인문대학", "자연대학"]
            assert values == [3.5, 3.2, 2.8]
            print("[PASS] Group by mean processed correctly")
        finally:
            os.unlink(csv_path)

    def test_process_group_by_sum(self):
        """group_by sum 처리"""
        from app.api.pandas_processor import process_group_by

        csv_path = self.setup_test_csv()
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)

            labels, values = process_group_by(df, "학과", "학생수", "sum")

            assert labels == ["공과대학", "인문대학", "자연대학"]
            assert values == [100, 80, 60]
            print("[PASS] Group by sum processed correctly")
        finally:
            os.unlink(csv_path)

    def test_process_invalid_columns_returns_empty(self):
        """유효하지 않은 컬럼명 시 빈 리스트 반환"""
        from app.api.pandas_processor import process_group_by

        csv_path = self.setup_test_csv()
        try:
            import pandas as pd
            df = pd.read_csv(csv_path)

            labels, values = process_group_by(df, "없는학과", "평점", "mean")

            assert labels == []
            assert values == []
            print("[PASS] Invalid columns return empty")
        finally:
            os.unlink(csv_path)

    def test_validate_processing_result_valid(self):
        """유효한 결과 검증"""
        from app.api.pandas_processor import validate_processing_result

        result = validate_processing_result(["a", "b"], [1, 2])
        assert result is True
        print("[PASS] Valid result passes validation")

    def test_validate_processing_result_empty(self):
        """빈 결과 검증"""
        from app.api.pandas_processor import validate_processing_result

        result = validate_processing_result([], [])
        assert result is False
        print("[PASS] Empty result fails validation")

    def test_validate_processing_result_all_zeros(self):
        """전부 0인 결과 검증"""
        from app.api.pandas_processor import validate_processing_result

        result = validate_processing_result(["a", "b"], [0, 0])
        assert result is False
        print("[PASS] All zeros fails validation")

    def test_process_time_series_monthly(self):
        """time_series 월별 처리"""
        from app.api.pandas_processor import process_time_series
        import pandas as pd

        df = pd.DataFrame({
            "date": ["2024-01-15", "2024-01-20", "2024-02-10", "2024-02-25", "2024-03-05", "2024-03-15"],
            "sales": [100, 150, 120, 200, 180, 220],
        })

        labels, values = process_time_series(df, "date", "sales", "monthly")

        assert len(labels) > 0, f"Expected labels but got: {labels}"
        assert len(values) > 0, f"Expected values but got: {values}"
        print(f"[PASS] Time series monthly processed: labels={labels}, values={values}")

    def test_process_time_series_invalid_column(self):
        """time_series 유효하지 않은 컬럼"""
        from app.api.pandas_processor import process_time_series
        import pandas as pd

        df = pd.DataFrame({"날짜": [], "매출": []})
        labels, values = process_time_series(df, "없는날짜", "매출", "monthly")

        assert labels == []
        assert values == []
        print("[PASS] Time series with invalid column returns empty")


class TestChartConfigGeneration:
    """chart config 생성 테스트"""

    def test_generate_bar_chart_config(self):
        """bar 차트 config 생성"""
        from app.api.graph_config import generate_chart_config

        config = generate_chart_config(
            chart_type="bar",
            labels=["공과대학", "인문대학"],
            series_data=[3.5, 3.2],
            title="평점 by 학과",
            x_axis_label="학과",
            y_axis_label="평점",
        )

        assert config["title"]["text"] == "평점 by 학과"
        assert config["xAxis"]["type"] == "category"
        assert config["xAxis"]["data"] == ["공과대학", "인문대학"]
        assert config["series"][0]["type"] == "bar"
        assert config["series"][0]["data"] == [3.5, 3.2]
        print("[PASS] Bar chart config generated")

    def test_generate_pie_chart_config(self):
        """pie 차트 config 생성"""
        from app.api.graph_config import generate_chart_config

        config = generate_chart_config(
            chart_type="pie",
            labels=["공과대학", "인문대학"],
            series_data=[3.5, 3.2],
            title="비율",
        )

        assert config["series"][0]["type"] == "pie"
        assert config["series"][0]["radius"] == "50%"
        print("[PASS] Pie chart config generated")

    def test_generate_line_chart_config(self):
        """line 차트 config 생성"""
        from app.api.graph_config import generate_chart_config

        config = generate_chart_config(
            chart_type="line",
            labels=["1월", "2월", "3월"],
            series_data=[100, 150, 120],
            title="월별 매출",
        )

        assert config["series"][0]["type"] == "line"
        assert config["series"][0]["smooth"] is True
        print("[PASS] Line chart config generated")

    def test_generate_scatter_chart_config(self):
        """scatter 차트 config 생성"""
        from app.api.graph_config import generate_chart_config

        config = generate_chart_config(
            chart_type="scatter",
            labels=["A", "B", "C"],
            series_data=[1.5, 2.3, 0.8],
            title="학사경고 vs 중도탈락률",
            x_axis_label="학사경고횟수",
            y_axis_label="중도탈락률",
        )

        assert config["title"]["text"] == "학사경고 vs 중도탈락률"
        assert config["xAxis"]["type"] == "category"
        assert config["xAxis"]["data"] == ["A", "B", "C"]
        assert config["series"][0]["type"] == "scatter"
        print("[PASS] Scatter chart config generated")

    def test_generate_heatmap_chart_config(self):
        """heatmap 차트 config 생성"""
        from app.api.graph_config import generate_chart_config

        config = generate_chart_config(
            chart_type="heatmap",
            labels=["A", "B", "C"],
            series_data=[[1, 2, 3], [4, 5, 6], [7, 8, 9]],
            title="상관관계 히트맵",
        )

        assert config["title"]["text"] == "상관관계 히트맵"
        assert config["xAxis"]["type"] == "category"
        assert config["series"][0]["type"] == "heatmap"
        print("[PASS] Heatmap chart config generated")


class TestGenerateChartPrompt:
    """LLM 프롬프트 생성 테스트"""

    def test_generate_chart_prompt_structure(self):
        """프롬프트에 analysis intent 요청 포함"""
        from app.api.insight_recommendation import generate_chart_prompt

        columns = [
            {"name": "학과", "data_type": "category"},
            {"name": "평점", "data_type": "number"},
        ]
        sample_data = [
            {"학과": "공과대학", "평점": 3.5},
            {"학과": "인문대학", "평점": 3.2},
        ]

        prompt = generate_chart_prompt(columns, 100, "학과별 평균 평점", sample_data)

        assert "analysis_type" in prompt
        assert "group_by" in prompt
        assert "JSON object" in prompt
        assert "CHART_CONFIG_START" not in prompt
        print("[PASS] Chart prompt requests analysis intent, not ECharts config")

    def test_generate_chart_prompt_for_relationship_request(self):
        """관계 요청 시 scatter/chart type 선택 가능한 프롬프트 생성"""
        from app.api.insight_recommendation import generate_chart_prompt

        columns = [
            {"name": "학사경고횟수", "data_type": "number"},
            {"name": "중도탈락률", "data_type": "number"},
        ]
        sample_data = [
            {"학사경고횟수": 1, "중도탈락률": 0.05},
            {"학사경고횟수": 2, "중도탈락률": 0.15},
        ]

        prompt = generate_chart_prompt(columns, 100, "학사경고와 중도탈락률간의 관계", sample_data)

        assert "analysis_type" in prompt
        assert "chart_type" in prompt
        print("[PASS] Chart prompt includes chart_type guidance for relationship requests")

    def test_parse_scatter_intent(self):
        """scatter intent JSON 파싱"""
        from app.api.insight_recommendation import parse_analysis_intent

        response = '{"analysis_type": "scatter", "x_col": "학사경고횟수", "y_col": "중도탈락률", "chart_type": "scatter"}'
        result = parse_analysis_intent(response)

        assert result is not None
        assert result["analysis_type"] == "scatter"
        assert result["chart_type"] == "scatter"
        print("[PASS] Scatter intent parsed correctly")


class TestEndToEnd:
    """end-to-end 통합 테스트"""

    def setup_test_csv(self):
        """테스트용 CSV 파일 생성"""
        content = """학과,평점,학생수
공과대학,3.5,100
인문대학,3.2,80
자연대학,2.8,60
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            return f.name

    def test_end_to_end_group_by_flow(self):
        """LLM → 파싱 → pandas → chart config 전체 흐름 (group_by)"""
        import pandas as pd
        from app.api.pandas_processor import load_csv_data, process_analysis_intent
        from app.api.graph_config import generate_chart_config

        csv_path = self.setup_test_csv()
        try:
            df = load_csv_data(csv_path)
            assert len(df) == 3

            intent = {
                "analysis_type": "group_by",
                "group_by": "학과",
                "value": "평점",
                "agg_func": "mean",
                "chart_type": "bar",
            }

            result = process_analysis_intent(df, intent)
            assert result is not None
            assert result["labels"] == ["공과대학", "인문대학", "자연대학"]
            assert result["values"] == [3.5, 3.2, 2.8]

            config = generate_chart_config(
                chart_type=result["chart_type"],
                labels=result["labels"],
                series_data=result["values"],
                title=result.get("title"),
                x_axis_label=result.get("x_axis_label"),
                y_axis_label=result.get("y_axis_label"),
            )

            assert config["series"][0]["type"] == "bar"
            assert config["xAxis"]["data"] == ["공과대학", "인문대학", "자연대학"]
            print("[PASS] End-to-end group_by flow completed")
        finally:
            os.unlink(csv_path)

    def test_end_to_end_with_mock_llm_intent(self):
        """Mock LLM intent로 chart config 생성"""
        import pandas as pd
        from app.api.pandas_processor import process_analysis_intent
        from app.api.graph_config import generate_chart_config

        content = """학과,평점
공과대학,3.5
인문대학,3.2
자연대학,2.8
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write(content)
            csv_path = f.name

        try:
            df = pd.read_csv(csv_path)

            mock_intent = {
                "analysis_type": "group_by",
                "group_by": "학과",
                "value": "평점",
                "agg_func": "mean",
                "chart_type": "bar",
                "title": "학과별 평균 평점",
                "x_axis_label": "학과",
                "y_axis_label": "평점",
            }

            result = process_analysis_intent(df, mock_intent)
            config = generate_chart_config(
                chart_type=result["chart_type"],
                labels=result["labels"],
                series_data=result["values"],
                title=result.get("title"),
                x_axis_label=result.get("x_axis_label"),
                y_axis_label=result.get("y_axis_label"),
            )

            assert config["title"]["text"] == "학과별 평균 평점"
            assert config["series"][0]["type"] == "bar"
            print("[PASS] End-to-end with mock LLM intent completed")
        finally:
            os.unlink(csv_path)


if __name__ == "__main__":
    print("=" * 60)
    print("ai-chart-data-processing Tests")
    print("=" * 60)

    test = TestAnalysisIntentParsing()
    print("\n[1] Analysis Intent Parsing Tests")
    for method in dir(test):
        if method.startswith("test_"):
            try:
                getattr(test, method)()
            except Exception as e:
                print(f"[FAIL] {method}: {e}")

    test = TestFallbackIntent()
    print("\n[2] Fallback Intent Tests")
    for method in dir(test):
        if method.startswith("test_"):
            try:
                getattr(test, method)()
            except Exception as e:
                print(f"[FAIL] {method}: {e}")

    test = TestPandasProcessing()
    print("\n[3] Pandas Processing Tests")
    for method in dir(test):
        if method.startswith("test_"):
            try:
                if method == "setup_test_csv":
                    continue
                getattr(test, method)()
            except Exception as e:
                print(f"[FAIL] {method}: {e}")

    test = TestChartConfigGeneration()
    print("\n[4] Chart Config Generation Tests")
    for method in dir(test):
        if method.startswith("test_"):
            try:
                getattr(test, method)()
            except Exception as e:
                print(f"[FAIL] {method}: {e}")

    test = TestGenerateChartPrompt()
    print("\n[5] Generate Chart Prompt Tests")
    for method in dir(test):
        if method.startswith("test_"):
            try:
                getattr(test, method)()
            except Exception as e:
                print(f"[FAIL] {method}: {e}")

    test = TestEndToEnd()
    print("\n[6] End-to-End Integration Tests")
    for method in dir(test):
        if method.startswith("test_"):
            try:
                if method == "setup_test_csv":
                    continue
                getattr(test, method)()
            except Exception as e:
                print(f"[FAIL] {method}: {e}")

    print("\n" + "=" * 60)
    print("Tests completed")
    print("=" * 60)
