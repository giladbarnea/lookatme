#!/usr/bin/env python3
import sys

dry_run = False
for arg in sys.argv[1:]:
    if arg == '--dry-run':
        dry_run = True
        break


def accumulate(*slides) -> str:
    acc = f"\n---\n"
    for i, slide in enumerate(slides):
        prev_slides = slides[:i]
        if prev_slides:
            acc += f"\n---\n" + ''.join(prev_slides) + f"{slide}\n"
        else:
            acc += f"{slide}\n"
    return acc


Screen = list[str]
Topic = list[Screen]


def main():
    header = """---
title: RSEvents
author: RSEvents Squad
date: 2021-08-04
styles:
    style: monokai
    table:
        column_spacing: 15
    margin:
        top: 1
        bottom: 1
    padding:
        top: 2
        bottom: 2
extensions: 
    - file_loader
    - terminal
    - image_ueberzug"""

    what_is_rsevents: Topic = [[
        "# What is RSEvents?\n## Overview\n",
        "`RSEvents` stands for RouterSecure Events, or HomeSecure Events.\n",
        """\nIt's responsible for processing device-related events coming from `HomeSecure`, """,
        """and relaying them other microservices.\n""",
        """\nExamples for such microservices: `Notifications`, `Accounts`, and `Buckets` (reader/writer).\n"""
        ],
        ["""# What is RSEvents?\n## Properties\n""",
         "\n- receives events from HomeSecure\n",
         "- interacts with account / device scope\n"
         ]
        ]
    tech_stack_proto1 = [
        "# Tech Stack - 1/3\n",
        "## google's `Protobuf`\n",
        "- (De)compresses complex data into lightweight bytes array (and back to workable data)\n",
        "  - encryption, faster, cheaper\n",
        "- Auto-generates code based on a pre-defined `.proto` scheme\n",
        "  - can be defined by product or architects (Hagai in our case)\n",
        "- Provides basic validation\n",
        "  - Types and structure of objects\n",
        "  - **Not** as granular as OpenAPI\n",
        ]
    tech_stack_proto2 = [
        """# Tech Stack - 1/3
## google's `Protobuf` - Example

A protobuf model defined by Hagai:\n""",
        """```proto
message DeviceEventLastSeen
{
  MessageBase message = 1;
  string last_seen = 2;
}```
""",
        "Is sent to RSEvents as:\n",
        r"""```python
b'\nQ\n\n1628071354\x12\x18f18uh-1L2/OY_}zfH0ipxxX?\x1a)\n\x0c94e420fc43e3\x12\x0e__GILAD_USER__\x1a\t__GILAD__\x12\tyesterday'
```
""",
        "And is unpacked into a normal json:\n",
        """```json
{
    "message" {
        "timestamp": "1628071354",
        "trace_id": "f18uh-1L2/OY_}zfH0ipxxX?",
        "device": {
            "device_id": "f18uh-1L2/OY_}zfH0ipxxX?",
            "user_id": "__GILAD_USER__",
            "account_id": "__GILAD__"
        },
    }
    "last_seen": "yesterday"
}
```""",
        ]

    tech_stack_kafka = [
        "# Tech Stack - 2/3\n## Good ol' Kafka\n",
        "- Consumes and parses the encoded bytestream into a legit JSON\n",
        "- Builds the appropriate `Pydantic` model",
        "        *an appropriate WHAT now?*\n",
        "- Lastly, publishes the model's output to `Notifications`, `Accounts`, and/or `Buckets`.",
        ]
    tech_stack_pydantic1 = [
        "# Tech Stack - 3/3\n## `Pydantic`\n",
        "A python library that plays really well with OpenAPI. \n",
        "- generates class definitions from an OpenAPI scheme, ",
        "which fully validate any received data (according to the scheme rules)\n",
        "- outputs the data back into a range of formats\n",
        "- requires the developer only to define the interface (type and structure), ",
        "while doing the implementation automagically. \n\n",
        "The respective Pydantic model:\n",
        """```python3
class DeviceEventLastSeen(pydantic.BaseModel):
    timestamp: str
    trace_id: Optional[Union[str, dict]]
    device_id: str
    user_id: str
    account_id: str
    last_seen: str    
```"""
        ]
    tech_stack_pydantic2 = [
        "# Tech Stack - 3/3\n## `Pydantic`\n",
        "Post-validation, the models optionally output specific objects,\n\n",
        "that conform, and get published away to the aforementioned microservices ",
        "(`Notifications`, `Accounts`, `Buckets`).",

        ]

    spotlight = [
        "# An example end-to-end flow\n",
        "## Processing data with `RSEvents` and sending a notification via `Notifications`\n",
        "### But first... \n",

        ]

    tech_stack: Topic = [tech_stack_proto1,
                         tech_stack_proto2,
                         tech_stack_kafka,
                         tech_stack_pydantic1,
                         tech_stack_pydantic2,
                         spotlight
                         ]
    notifications = [[
        "# New `Notifications` under `RSEvents` - Feature Overview\n",
        "HomeSecure backend events may trigger manager notifications.\n\n",
        "For demonstration purposes, these notifications are separated into two groups:\n",
        "\n1. New (non-existing previously) manager notifications.\n",
        "2. Existing notifications."
        ],
        [
            "# HomeSecure events and their corresponding notifications: Existing vs New\n",
            "![25](assets/e2n-table.png)"
            ],
        [
            "# A new Notification model (built by `DeviceEventLastSeen`):\n",
            """```python
class DeviceInActiveDeleted(BaseNotification):
   type_ = 'device_inactive_deleted  
   level = 'device'
   def __init__(self, account_id, user_id, device_id):
       data = {
           'account_id': account_id,
           'user_id': user_id,
           'device_id': device_id,
       }
       service_id = 'general'
       super().__init__(
           data,
           service_id,
           self.type_,
       )
```\n""",
            'After the event is processed by `RSEvents`, the notifications are instantiated, and are published via kafka to `as-notifications-incoming-topic`.\n',
            ],
        [
            "# Here is a chart that demonstrates this whole flow:\n",
            "![34](assets/diagrams/notification_demo_flow_black.png)\n",
            ],
        [
            "# Live demo! \n",
            "![5](assets/chibur.png)\n",
            ]]
    topics: list[Topic] = [
        what_is_rsevents,
        tech_stack,
        notifications
        ]
    screens = []
    from itertools import chain
    for i, screen in enumerate(chain(*topics)):
        acc = accumulate(*screen)
        screens.append(acc)
    if dry_run:
        [print(screen) for screen in screens]
        print('DRY RUN')
    else:
        with open('./demo-compiled.md', mode='w') as md:
            md.write(header)
            md.write('\n'.join(screens))
        print('Compiled to ./demo-compiled.md')


if __name__ == '__main__':
    print('Compiling demo...')
    main()
