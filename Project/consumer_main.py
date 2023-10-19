from Consumer import Consumer
from util import Commands

def main():
    cons = Consumer()
    print(f"Consumer - [{cons.cons_id}] - setup complete.")
    print("cmd:")
    print(f"- {Commands.SUB.value} [pid] Optional[sid] - subscribe to producer pid, stream sid")
    print(f"- {Commands.UNSUB.value} [pid] Optional[sid] - unsubscribe from producer pid, stream sid")
    print(f"- {Commands.EXIT.value} - end program")

    while True:
        print("-" * 10)
        cmd = input(f"Consumer - {cons.cons_id} - waiting on input ...\n> ").split()

        if cmd[0] == Commands.SUB.value:
            if len(cmd) == 3:
                # sub to specific stream
                cons.subscribe_stream(cmd[1], cmd[2])
            elif len(cmd) == 2:
                cons.subscribe_producer(cmd[1])
            else:
                print("Invalid Command")
                continue 
        elif cmd[0] == Commands.UNSUB.value:
            if len(cmd) == 3:
                cons.unsubscribe_stream(cmd[1], cmd[2])
            elif len(cmd) == 2:
                cons.unsubscribe_producer(cmd[1])
            else:
                print("Invalid Command")
                continue
        elif cmd[0] == Commands.EXIT.value:
            exit()
        else:
            print("Invalid Command")



if __name__ == "__main__":
    main()