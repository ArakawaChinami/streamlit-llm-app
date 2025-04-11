from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

# 環境変数をロード
load_dotenv()

# LLMからの回答を取得する関数
def get_llm_response(user_input: str, expert_type: str) -> str:
    """
    入力テキストと専門家の種類を基にLLMからの回答を取得する。

    Args:
        user_input (str): ユーザーが入力したテキスト。
        expert_type (str): 専門家の種類（例: "パンの専門家", "バイオリンの専門家"）。

    Returns:
        str: LLMからの回答。
    """
    # LangChain ChatOpenAIの初期化
    llm = ChatOpenAI(temperature=0.7)

    # 専門家の種類に応じたシステムメッセージを設定
    if expert_type == "パンの専門家":
        system_message = SystemMessage(content="あなたはパンの専門家です。パンの製造、種類、歴史、レシピについての質問に答えてください。")
    elif expert_type == "バイオリンの専門家":
        system_message = SystemMessage(content="あなたはバイオリンの専門家です。バイオリンの演奏、歴史、製作、メンテナンスについての質問に答えてください。")
    else:
        raise ValueError("無効な専門家の種類が選択されました。")

    # ユーザーの質問をHumanMessageとして渡す
    human_message = HumanMessage(content=user_input)

    # LLMに問い合わせて結果を取得
    response = llm([system_message, human_message])
    return response.content

# Streamlitアプリのタイトル
st.title("専門家に質問するアプリ")

# 専門家の種類を選択するラジオボタン
expert_type = st.radio(
    "専門家の種類を選択してください:",
    ("パンの専門家", "バイオリンの専門家")
)

# 入力フォーム
user_input = st.text_input("質問を入力してください:")

# 入力がある場合、LLMにプロンプトを渡して結果を表示
if st.button("送信"):
    if user_input.strip():
        with st.spinner("専門家に問い合わせ中..."):
            try:
                # 関数を利用してLLMからの回答を取得
                response = get_llm_response(user_input, expert_type)
                st.success("専門家からの回答:")
                st.write(response)
            except ValueError as e:
                st.error(f"エラー: {e}")
    else:
        st.error("質問を入力してください。")
