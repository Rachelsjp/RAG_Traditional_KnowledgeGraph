import streamlit as st
from rag_query import get_rag_answer
from graph_query import find_dashboards, find_dependencies, find_source_system


st.set_page_config(page_title="RAG Comparison", layout="wide")

st.title("AI Data Pipeline Impact Analyzer")

st.write("Compare Traditional RAG vs Knowledge Graph RAG")


question = st.text_input("Ask a question about your data pipeline")


# detect table names automatically
tables = ["fact_orders","dim_customer","dim_product"]


def detect_table(q):
    for t in tables:
        if t in q.lower():
            return t
    return None


if question:

    col1, col2 = st.columns(2)

    table = detect_table(question)

    # --------------------
    # Traditional RAG
    # --------------------
    with col1:

        st.subheader("Traditional RAG Answer")

        try:
            with st.spinner("Generating response..."):  # ✅ only addition (no UI change impact)
                answer = get_rag_answer(question)
            st.write(answer)

        except Exception as e:
            st.error(e)


    # --------------------
    # Graph RAG
    # --------------------
    with col2:

        st.subheader("Graph RAG Answer")

        try:

            if table is None:
                st.warning("No table detected in question")

            else:

                q_lower = question.lower()  # ✅ improvement (no UI impact)

                if "depend" in q_lower or "dependency" in q_lower:
                    results = find_dependencies(table)

                elif "feed" in q_lower or "source" in q_lower:
                    results = find_source_system(table)

                else:
                    results = find_dashboards(table)


                if results:

                    for r in results:
                        st.success(r)

                else:

                    st.warning("No results found")

        except Exception as e:
            st.error(e)