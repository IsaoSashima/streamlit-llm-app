from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

load_dotenv() # app.pyにLLMとやり取りする（OpenAI APIを呼びだすコード）を記述して実行すると、「.env」ファイルに記載した環境変数（ここではOpenAI APIキー）が自動で参照されるようになる

st.title("専門家に聞いてみよう！")

st.write("##### 専門家①：料理専門家")
st.write("具材を入力すると、それを使ったレシピを提案します。")
st.write("##### 専門家②：翻訳家")
st.write("翻訳したいテキストを入力すると英語に翻訳します。")

selected_item = st.radio(
    "専門家を選択してください。",
    ["専門家①：料理専門家", "専門家②：翻訳家"]
)

st.divider()

def propose_recipe(ingredients):
    # 受け取った具材を含めてLLMにレシピを提案させて、その回答を受け取る処理を記述する
    template = """
    あなたは料理の専門家です。以下の具材を使ったレシピを提案してください。もしも具材が食べ物ではない場合は、食べ物を入力するように促す文章を生成してください。
    具材: {ingredients}
    """

    llm = ChatOpenAI(model_name = "gpt-4o-mini", temperature = 0.5)
    messages = [
        SystemMessage(content = "You are a cooking expert. Please suggest a recipe using the following ingredients."),
        HumanMessage(content = template)
    ]
    result = llm(messages)
    return result.content
    

def propose_translation(text):
    # 受け取ったテキストを含めてLLMに翻訳を提案させて、その回答を受け取る処理を記述する
    template = """
    あなたは翻訳家です。以下のテキストを英語に翻訳してください。
    テキスト: {text}
    """

    llm = ChatOpenAI(model_name = "gpt-4o-mini", temperature = 0.5)
    messages = [
        SystemMessage(content = "You are a translator. Please translate the following text into English."),
        HumanMessage(content = template)
    ]

    result = llm(messages)
    return result.content

if selected_item == "専門家①：料理専門家":
    input_message = st.text_input("具材を入力してください。", placeholder="例：鶏肉、玉ねぎ、にんじん")
    recipe = propose_recipe(input_message)
else:
    input_message = st.text_input("翻訳したいテキストを入力してください。", placeholder="例：こんにちは、元気ですか？")
    translation = propose_translation(input_message)


if st.button("送信"):
    st.divider()

    if selected_item == "専門家①：料理専門家":
        if input_message:
            st.write(recipe)

        else:
            st.error("具材を入力してください。")

    else:
        if input_message:
            st.write(translation)

        else:
            st.error("翻訳したいテキストを入力してください。")
