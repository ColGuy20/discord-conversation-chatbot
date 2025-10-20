import sys, traceback, api
import commands as cmd
import webserver as ws

#--Main--

if __name__ == "__main__":
    api.prime_imports()

    server, thread = ws.start_web_server()
    print("[LOG] Web server is active on port 8080")

    try:
        cmd.run_bot()
    except KeyboardInterrupt:
        print("[LOG] Shutting down from host")
    except Exception:
        traceback.print_exc()
        import time; time.sleep(20)
        sys.exit(1)
    finally:
        try:
            ws.stop_web_server(server)
        finally:
            thread.join(timeout=2)
        print("[LOG] Web server shut down") 
