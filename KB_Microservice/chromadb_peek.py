import chromadb
from chromadb.config import Settings
from pprint import pprint as pp


persist_directory = "chromadb"
chroma_client = chromadb.Client(Settings(persist_directory=persist_directory,chroma_db_impl="duckdb+parquet",))
collection = chroma_client.get_or_create_collection(name="knowledge_base")

print('KB presently has %s entries' % collection.count())
print('\n\nBelow are the top 10 entries:')
results = collection.peek()

# results = collection.query(query_texts=["EsmetheCatsVomitingIssues"], n_results=5)
# results = collection.get(ids=["43016976-3994-486e-bb77-4e841801149f"])
pp(results)