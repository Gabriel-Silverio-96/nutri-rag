import streamlit as st

from nutri_rag.rag import answer_question, build_index


@st.cache_resource(show_spinner=False)
def load_index():
    return build_index()


def main() -> None:
    st.set_page_config(page_title="Nutri RAG", page_icon="🥗", layout="centered")
    st.title("🥗 Nutri RAG")
    st.caption("Faça perguntas sobre alimentação e nutrição com base nos documentos do projeto.")

    with st.form("question_form"):
        question = st.text_area(
            "Sua pergunta",
            placeholder="Ex.: Quais são as diferenças entre margarina e manteiga?",
            height=100,
        )
        submitted = st.form_submit_button("Consultar", type="primary")

    if submitted:
        question = question.strip()
        if not question:
            st.warning("Digite uma pergunta para consultar o RAG.")
            return

        st.session_state.pop("answer", None)
        st.session_state.pop("sources", None)
        try:
            with st.spinner("Buscando trechos relevantes e preparando a resposta..."):
                index = load_index()
                answer, sources = answer_question(question, index)
            st.session_state["question"] = question
            st.session_state["answer"] = answer
            st.session_state["sources"] = sources
        except Exception as error:
            st.error(f"Não foi possível consultar o RAG: {error}")

    if st.session_state.get("answer"):
        st.subheader("Resposta")
        st.markdown(st.session_state["answer"])
        sources = st.session_state.get("sources", [])
        if sources:
            with st.expander("Fontes consultadas"):
                for source in sources:
                    st.markdown(f"- {source}")

    with st.sidebar:
        st.header("Sobre")
        st.write(
            "O Nutri RAG consulta os PDFs de alimentação e nutrição disponíveis no projeto. "
            "Quando a informação não está nos documentos, a resposta deve indicar essa limitação."
        )
        if st.button("Recarregar índice"):
            load_index.clear()
            st.rerun()


if __name__ == "__main__":
    main()
