import commands as cmd
import webserver as ws

#--Main--

if __name__ == "__main__":
    server, thread = ws.start_web_server()
    print("Health web server running on port 8080")

    try:
        cmd.run_bot()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        try:
            ws.stop_web_server(server)
        finally:
            thread.join(timeout=2)
        print("Web server stopped.") 
