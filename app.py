import panel as pn
from llm import ask_gemini
# from search import vector_search, semantic_search, bm25_search
from regulation_search import RegulationSearch

pn.extension()

query_input = pn.widgets.TextAreaInput(placeholder="Ask a question about Regulation DD...", width=900, height=100)
output = pn.pane.Markdown("", width=600)

def run_search(event):
    searcher = RegulationSearch()
    query = query_input.value
    # bm_results = searcher.semantic_search(query)
    bm_results = searcher.bm25_search(query)
    vector_results = searcher.vector_search(query)
    context = '\n\n'.join(bm_results[:3] + vector_results[:3])
    prompt = f"Given the following excerpts from Regulation DD:\n\n{context}\n\nAnswer the question: {query}"
    answer = ask_gemini(prompt)
    output.object = f"### Answer:\n{answer}\n\n---\n### Context:\n{context}"

search_btn = pn.widgets.Button(name="Search", button_type="primary")
search_btn.on_click(run_search)

pn.Column("# Regulation DD Search",
          query_input,
          search_btn,
          output).servable()
