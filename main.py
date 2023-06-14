from tkinter import *
from vsm import *
import timeit
import os

results = []
query = None

stop_words = stopWordList("Stopword-List.txt")
docs_tokens = documentTokenizer(30, stop_words)
extract_documents = get_document_extracts(30)
inverted_index = invertedIndex(docs_tokens)
doc_vectors =documnetVector(docs_tokens,inverted_index)

def clicked():
    start_time = timeit.default_timer()
    global query
    global results
    query = searchQuery.get()
    searchQuery.delete(0, END)
    # query = "cricket politics"
    query_tokens = queryProcessing(query, stop_words)
    query_vector = queryVector(query,stop_words,inverted_index)
    results = cosineSimalirity(doc_vectors,query_vector,query_tokens)
    # results = sorted(results.items(), key=lambda x: x[1], reverse=True)
    
    # for doc_id, score in results:
    #     print(f"Document {doc_id}:  (score={score:.4f})")

    searchStats.config(
        text=f'Processed {(docs_tokens.count)} documents in {len(inverted_index.keys())}ms , fetched {len(results)} results')
    for label in scrollable_frame.winfo_children():
        label.destroy()
    for i, (doc_id, score) in enumerate(results):
        try:
            if score ==0:
                continue
            label_text = f"Document {doc_id}: extract \"{extract_documents[int(doc_id)-1]}\" (score={score:.4f})"
            label = Label(scrollable_frame, text=label_text,
                        anchor="w", wraplength=450)
            label.pack(pady=5, padx=10)

            label.bind("<Button-1>", lambda event,
                    index=int(doc_id)-1: open_file(index))

        except ValueError:
            pass


    end_time = timeit.default_timer()
    execution_time_in_microseconds = (end_time - start_time) * 1_000_000
    searchStats.config(text=f'Search result for {query} \nProcessed in {execution_time_in_microseconds} ms , fetched {len([val for _, val in results if val != 0])} results')


def open_file(index):
    # set the exact path of the folder dataset
    file_name = f"E:/study/IR/IR assignment 2/Dataset/{index+1}.txt"
    os.startfile(file_name)


window = Tk()
window.title("VSM")
window.geometry('500x500')
window.resizable(False, False)

window.configure(bg="#f5f5f5")

exampleHeading = Label(
    window,
    text="Write your query like \"cricket politics\"",
    font=("Arial", 8),
    fg="#333",
    bg="#f5f5f5"
)
exampleHeading.grid(column=0, row=0, columnspan=2, pady=10, padx=100)

header_label = Label(
    window,
    text="Search Here",
    font=("Arial Bold", 20),
    fg="#333",
    bg="#f5f5f5"
)
header_label.grid(column=0, row=1)

searchQuery = Entry(
    window,
    width=50,
    font=("Arial", 10),
    bd=0,
    bg="#f9f9f9",
    highlightcolor="#333",
    highlightthickness=1,
    highlightbackground="#ccc"
)
searchQuery.grid(column=0, row=2, padx=100)

searchStats = Label(
    window,
    text="Welcome",
    font=("Arial Bold", 8),
    fg="#333",
    bg="#f5f5f5"
)
searchStats.grid(column=0, row=3)

searchBtn = Button(
    window,
    text="Search",
    font=("Arial Bold", 14),
    bg="#333",
    fg="#fff",
    bd=0,
    activebackground="#555",
    activeforeground="#fff",
    command=clicked
)
searchBtn.grid(column=0, row=4, padx=100, pady=10)

canvas = Canvas(window, width=500, height=400, bg="#fff")
scrollbar = Scrollbar(window, orient=VERTICAL, command=canvas.yview)
scrollable_frame = Frame(canvas, bg="#fff")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)


canvas.grid(column=0, row=5, sticky="nsew")
scrollbar.grid(column=1, row=5, sticky="ns")

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(5, weight=1)

window.mainloop()

