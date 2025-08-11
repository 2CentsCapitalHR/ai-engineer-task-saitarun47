import json
from pathlib import Path
import streamlit as st
from main import build_agent
from main import analyze_with_agno , add_inline_comments
from utils import extract_text , classify_doc_type , infer_process , checklist_for_process 

st.set_page_config(page_title="ADGM Corporate Agent",layout="centered")
st.title("ADGM Corporate Agent")


st.subheader("Upload .docx files")
uploads = st.file_uploader("Upload one or more .docx documents",type=["docx"],accept_multiple_files=True)

st.subheader("Build/load ADGM knowledge")
agent = None
if st.button("Initialize Agent",type="primary"):
    with st.spinner("building vector index and initializing agent.."):
        agent=build_agent()
        st.session_state["agent"] = agent
    st.success("Agent ready")
elif "agent" in st.session_state:
    agent= st.session_state["agent"]

results = []
if uploads and agent:
    st.subheader("analysing uploaded documents..")

    doc_types = []
    parsed_docs = []
    for f in uploads:
        file_bytes = f.read()
        text = extract_text(file_bytes)
        dtype = classify_doc_type(f.name,text)
        doc_types.append(dtype)
        parsed_docs.append({"name":f.name , "bytes":file_bytes, "text":text, "type":dtype})

    process = infer_process(doc_types)
    checklist = checklist_for_process(process)
    uploaded_types = set(doc_types)
    missing = [req for req in checklist if req not in uploaded_types]

    if process=="Company Incorporation":
        st.markdown("### Checklist verification")
        st.write(f"Required docs: {len(checklist)} | Uploaded matching types: {len(uploaded_types & set(checklist))}")
        if missing:
            st.error(f"Missing mandatory documents: {', '.join(missing)}")
        else:
            st.success("All mandatory documents are present")
    
    st.markdown("### Analysis")
    for d in parsed_docs:
        with st.spinner("reviewing.."):
            issues = analyze_with_agno(agent,d["text"])
        reviewed_bytes = add_inline_comments(d["bytes"],issues)

        per_report = {
            "document": d["name"],
            "type": d["type"],
            "process":process,
            "issues_found": issues,
        }
        results.append(per_report)

        c1,c2 = st.columns(2)
        with c1:
            st.download_button(
                label=f"download reviewed docx",
                data = reviewed_bytes,
                file_name=f"reviewed_{d['name']}",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )

        with c2:
            st.download_button(
                label=f"Download json report",
                data=json.dumps(per_report,indent=2),
                file_name=f"{Path(d['name']).stem}.json",
                mime="application/json",
            )

if uploads and agent and results:
    st.subheader("Results:")
    agg_process = results[0].get("process","Unknown")
    req_docs = len(checklist_for_process(agg_process))
    uploaded_types=set([r["type"] for r in results])
    missing_docs = [d for d in checklist_for_process(agg_process) if d not in uploaded_types]

    aggregate = {
        "process": agg_process,
        "documents_uploaded": len(results),
        "required_documents": req_docs,
        "missing_documents": missing_docs,
        "files": results,

    }
    st.code(json.dumps(aggregate,indent=2),language="json")
    st.download_button(
        label="download json report",
        data=json.dumps(aggregate, indent=2),
        file_name="report.json",
        mime="application/json",
    )
st.markdown("-----")


    


