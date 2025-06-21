

import streamlit as st
from ai_agents.writer import spin_content
from ai_agents.reviewer import review_content
from vector_store import save_version, get_versions_by_chapter

st.set_page_config(page_title="Auto-Book Workflow", layout="wide")
st.title("📘 Auto-Book Workflow (AI-Powered)")


prompt = st.text_area("📥 Enter your raw chapter content:", height=200)
chapter_number = st.number_input("📚 Chapter Number", min_value=1, step=1)


if st.button("✨ Rewrite and Review"):
    if prompt.strip():
        version_id_prefix = f"chapter{chapter_number}"

        
        save_version(prompt, "original", chapter_number, version_id=f"{version_id_prefix}_original")

        
        with st.spinner("🔄 Rewriting chapter with AI..."):
            rewritten = spin_content(prompt)
            st.success("✅ Rewritten Chapter:")
            st.text_area("📖 Rewritten Chapter", rewritten, height=300)
            save_version(rewritten, "ai_rewritten", chapter_number, version_id=f"{version_id_prefix}_ai_rewritten")

        
        with st.spinner("🧐 Reviewing rewritten chapter..."):
            review = review_content(rewritten)
            st.success("✅ Review Suggestions:")
            st.text_area("📝 Suggestions & Improvements", review, height=300)
            save_version(review, "ai_review", chapter_number, version_id=f"{version_id_prefix}_ai_review")

        
        combined_text = f"Rewritten Chapter:\n{rewritten}\n\nReview Suggestions:\n{review}"
        st.download_button("⬇️ Download AI Output", combined_text, file_name="ai_chapter_review.txt")
    else:
        st.warning("⚠️ Please enter a valid chapter.")


st.markdown("---")
st.subheader("🧑‍💻 Final Human-Edited Version")

human_final = st.text_area("✏️ Paste your final edited chapter here (after AI suggestions)", height=200)

if st.button("💾 Save Final Human Version"):
    if human_final.strip():
        version_id_prefix = f"chapter{chapter_number}"
        save_version(human_final, "human_final", chapter_number, version_id=f"{version_id_prefix}_human_final")
        st.success("✅ Final version saved to ChromaDB.")
    else:
        st.warning("⚠️ Final version is empty.")


st.markdown("---")
st.subheader("📂 View All Versions for This Chapter")

if st.button("🔍 View All Versions for This Chapter"):
    result = get_versions_by_chapter(chapter_number)
    if result["documents"]:
        for i, doc in enumerate(result["documents"][0]):
            stage = result["metadatas"][0][i]["stage"]
            st.markdown(f"**🔸 Version {i+1} ({stage})**")
            st.text_area("", doc, height=200, key=f"version_{i}")
    else:
        st.info("ℹ️ No versions found for this chapter.")


st.markdown("---")
st.subheader("🔎 Intelligent Version Retrieval")

search_query = st.text_input("🔍 Enter your query to search relevant versions (e.g., 'explain CNNs')")

if st.button("🔎 Search"):
    if search_query.strip():
        from vector_search import search_relevant_versions
        results = search_relevant_versions(search_query, chapter_number)

        if results:
            st.success(f"✅ Found {len(results)} relevant versions (Top 3 shown):")
            for i, (score, doc, meta, id_) in enumerate(results[:3]):
                st.markdown(f"**🔸 Version {i+1}**")
                st.markdown(f"**Stage:** {meta['stage']} | **ID:** {id_} | **Score:** {score:.4f}")
                st.text_area("📄 Content", doc, height=200, key=f"search_result_{i}")
        else:
            st.warning("⚠️ No relevant versions found.")
    else:
        st.info("ℹ️ Please enter a valid query.")
