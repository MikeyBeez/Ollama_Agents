from langchain_community.tools import DuckDuckGoSearchRun

class DDGSearch:
    def __init__(self):
        self.search = DuckDuckGoSearchRun()

    def run_search(self, query):
        try:
            results = self.search.run(query)
            if isinstance(results, str):
                results_list = results.split("\n")
            else:
                results_list = results
            return results_list
        except Exception as e:
            print(f"Error: {e}")
            return []

