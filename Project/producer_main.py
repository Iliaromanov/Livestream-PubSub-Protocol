from Producer import Producer
from util import Commands

def main():
    prod = Producer()
    print(f"ProducerID - {prod.prod_id} - setup complete.")
    print("cmd:")
    print(f"- {Commands.PUB.value} [sid] - publish stream with id sid")
    print(f"- {Commands.STREAM.value} [path] - stream frames located at path")
    print("- exit - end program")
    
    while True:
        cmd = input(f"Producer - {prod.prod_id} - waiting on input ...\n> ").split()

        if cmd[0] == Commands.PUB.value:
            sid = cmd[1]
            prod.publish_new_stream(sid)
        elif cmd[0] == Commands.STREAM.value:
            pass
        elif cmd[0] == Commands.EXIT.value:
            exit()
        else:
            print("Invalid Command")



if __name__ == "__main__":
    main()