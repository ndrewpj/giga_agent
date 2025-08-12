build_graph:
	langgraph build -t giga_agent -c backend/graph/langgraph.json

init_files:
	cp -R backend/repl/files ./files/
