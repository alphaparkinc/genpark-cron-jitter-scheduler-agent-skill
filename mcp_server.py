"""MCP Server for Cron Jitter Scheduler Agent.
100% Python Standard Library JSON-RPC.
"""
import sys
import json
from client import CronJitterScheduler

def main():
    while True:
        line = sys.stdin.readline()
        if not line:
            break
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")

            if method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [
                            {
                                "name": "matches_cron",
                                "description": "Check if current or target datetime satisfies 5-part cron expression",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "cron_expr": {"type": "string", "description": "Standard 5-part crontab expression"}
                                    },
                                    "required": ["cron_expr"]
                                }
                            },
                            {
                                "name": "calculate_jittered_delay",
                                "description": "Calculate decorrelated jitter delay for distributed agents",
                                "inputSchema": {
                                    "type": "object",
                                    "properties": {
                                        "base_seconds": {"type": "number"},
                                        "jitter_ratio": {"type": "number", "default": 0.2},
                                        "seed_str": {"type": "string", "default": "agent"}
                                    },
                                    "required": ["base_seconds"]
                                }
                            }
                        ]
                    }
                }
            elif method == "tools/call":
                call_name = req.get("params", {}).get("name")
                args = req.get("params", {}).get("arguments", {})
                if call_name == "matches_cron":
                    res = {"matches": CronJitterScheduler.matches(args.get("cron_expr"))}
                elif call_name == "calculate_jittered_delay":
                    res = {"delay_seconds": CronJitterScheduler.calculate_jittered_delay(
                        base_seconds=args.get("base_seconds"),
                        jitter_ratio=args.get("jitter_ratio", 0.2),
                        seed_str=args.get("seed_str", "agent")
                    )}
                else:
                    res = {"error": "Unknown tool"}
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
