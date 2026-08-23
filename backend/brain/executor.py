from tools.registry import run_tool


class TaskExecutor:
    def execute(self, plan):
        results = {}
        steps = []

        for step in plan:
            args = [self._resolve_arg(arg, results) for arg in step.get("args", [])]
            result = run_tool(step["tool"], *args)
            results[step["save_as"]] = result
            steps.append({
                "tool": step["tool"],
                "success": self._is_success(result),
                "result": result,
            })

            if not self._is_success(result):
                break

        return {
            "success": all(step["success"] for step in steps),
            "steps": steps,
            "results": results,
        }

    def _resolve_arg(self, arg, results):
        if isinstance(arg, dict) and "from" in arg and "field" in arg:
            return results[arg["from"]][arg["field"]]

        return arg

    def _is_success(self, result):
        if isinstance(result, dict) and "success" in result:
            return result["success"]

        return result is not None
