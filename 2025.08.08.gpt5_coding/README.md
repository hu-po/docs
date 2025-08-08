![thumbnail](thumbnail.jpg)

# GPT5 Coding

### Links

**YouTube:** https://youtube.com/live/xiJwgwoiXpc

**X:** https://x.com/i/broadcasts/1ynKOlMXMVWGR

### References

- https://arcprize.org/leaderboard
- https://pbs.twimg.com/media/Gxw9EpRbsAMqC_q.jpg
- https://github.com/anthropics/claude-code
- https://github.com/sst/opencode
- https://cdn.openai.com/pdf/419b6906-9da6-406c-a19d-1bb078ac7637/oai_gpt-oss_model_card.pdf
- https://github.com/ollama/ollama

coding challenge:

#### basic

> create a text ui for the tatbot nodes. See src/conf/nodes.yaml for a list of nodes. Some nodes have a gpu, some only have a cpu. I want the TUI to show the memory usage of the gpus, the load on the cpus, and indicate which nodes are on and running. put all of your code in the src/tui-MODEL directory, don't touch the rest of the codebase. include documentation for the tui also in the src/tui-MODEL directory.

#### extras

> if nodes have MCP servers, I want to show those as being available. mcp servers are started with scripts/run_mcp.sh.
> evaluate the performance hit of the tui on each of the nodes
> display the node ip addresses
> show the nfs directory which is shared accross all nodes