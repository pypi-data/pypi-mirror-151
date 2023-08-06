# Python gRPC Client for EventStoreDB

This package provides a Python gRPC client for
[EventStoreDB](https://www.eventstore.com/). It has been
developed and tested to work with version 21.10 of EventStoreDB,
and with Python versions 3.7, 3.8, 3.9, and 3.10.

## Installation

Use pip to install this package from the
[the Python Package Index](https://pypi.org/project/esdbclient/).

    $ pip install esdbclient

It is recommended to install Python packages into a Python virtual environment.

## Getting started

### Start EventStoreDB

Use Docker to run EventStoreDB from the official container image on DockerHub.

    $ docker run -d --name my-eventstoredb -it -p 2113:2113 -p 1113:1113 eventstore/eventstore:21.10.2-buster-slim --insecure

### Construct client

The class `EsdbClient` can be constructed with a `uri` that indicates the hostname
and port number of the EventStoreDB server.

```python
from esdbclient.client import EsdbClient

client = EsdbClient(uri='localhost:2113')
```

### Append events

The method `append_events()` can be used to append events to
a stream. The arguments `stream_name`, `expected_position` and `new_events`
are required. The `stream_name` is a string. The `stream_position`
is an optional integer: an integer representing the expected current
position of the stream; or `None` if the stream is expected not to exist.
The `events` argument is a list of new event objects to be appended to the
stream. The class `NewEvent` can be used to construct new event objects.

The method `append_events()` returns the "commit position", which is a
monotonically increasing integer representing the position of the recorded
event in a "total order" of all recorded events in all streams.

```python
from uuid import uuid4

from esdbclient.client import NewEvent

# Construct new event object.
event1 = NewEvent(type="OrderCreated", data=b"{}")

# Define stream name.
stream_name1 = str(uuid4())

# Append list of events to new stream (expected_position=None).
commit_position1 = client.append_events(
    stream_name=stream_name1, expected_position=None, events=[event1]
)
```

The sequence of stream positions is gapless and zero-based, so the
expected position of the stream after appending the first event is
zero. The method `get_stream_position()` can be used to obtain the
current position of the stream.

```python
current_position = client.get_stream_position(stream_name=stream_name1)

assert current_position == 0
```

```python
event2 = NewEvent(type="OrderUpdated", data=b"{}")
event3 = NewEvent(type="OrderDeleted", data=b"{}")

commit_position2 = client.append_events(
    stream_name1, expected_position=0, events=[event2, event3]
)
```

### Read stream events

The method `read_stream_events()` can be used to read the recorded
events in a stream. The argument `stream_name` is required. By default,
all recorded events in the stream are returned in the order they were
appended. An iterable object of recorded events is returned.

Read all the recorded events in a stream.

```python
events = list(client.read_stream_events(stream_name=stream_name1))

assert len(events) == 3

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 0
assert events[0].type == event1.type
assert events[0].data == event1.data

assert events[1].stream_name == stream_name1
assert events[1].stream_position == 1
assert events[1].type == event2.type
assert events[1].data == event2.data

assert events[2].stream_name == stream_name1
assert events[2].stream_position == 2
assert events[2].type == event3.type
assert events[2].data == event3.data
```

The method `read_stream_events()` also supports three optional arguments,
`position`, `backwards`, and `limit`.

The argument `position` is an optional integer that can be used to indicate
the stream position from which to start reading. This argument is `None` by default,
meaning that the stream will be read from the start, or from the end if `backwards`
is `True`.

The argument `backwards` is a boolean which is by default `False` meaning the
stream will be read forwards by default, so that events are returned in the
order they were appended, If `backwards` is `True`, the stream will be read
backwards, so that events are returned in reverse order.

The argument `limit` is an integer which limits the number of events that will
be returned.

Read recorded events in a stream from a specific stream position.

```python
events = list(client.read_stream_events(stream_name1, position=1))

assert len(events) == 2

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 1
assert events[0].type == event2.type
assert events[0].data == event2.data

assert events[1].stream_name == stream_name1
assert events[1].stream_position == 2
assert events[1].type == event3.type
assert events[1].data == event3.data
```

Read the recorded events in a stream backwards from the end.

```python
events = list(client.read_stream_events(stream_name1, backwards=True))

assert len(events) == 3

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 2
assert events[0].type == event3.type
assert events[0].data == event3.data

assert events[1].stream_name == stream_name1
assert events[1].stream_position == 1
assert events[1].type == event2.type
assert events[1].data == event2.data
```

Read a limited number of recorded events in stream.

```python
events = list(client.read_stream_events(stream_name1, limit=2))

assert len(events) == 2

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 0
assert events[0].type == event1.type
assert events[0].data == event1.data

assert events[1].stream_name == stream_name1
assert events[1].stream_position == 1
assert events[1].type == event2.type
assert events[1].data == event2.data
```

Read a limited number of recorded events backwards from given position.

```python
events = list(client.read_stream_events(stream_name1, position=2, backwards=True, limit=1))

assert len(events) == 1

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 2
assert events[0].type == event3.type
assert events[0].data == event3.data
```

### Get current stream position

The method `get_stream_position()` can be used to get the current
position of the stream. This is the stream position of the last
event in the stream.

```python
current_position = client.get_stream_position(stream_name1)

assert current_position == 2
```

### Read all recorded events

The method `read_all_events()` can be used to read all recorded events
in all streams in the order they were committed. An iterable object of
recorded events is returned.

Read events from all streams in the order they were committed.

```python
events = list(client.read_all_events())

assert len(events) >= 3
```

The method `read_stream_events()` supports three optional arguments,
`position`, `backwards`, and `limit`.

The argument `position` is an optional integer that can be used to indicate
the commit position from which to start reading. This argument is `None` by default,
meaning that all the events will be read from the start, or from the end if `backwards`
is `True`.

The argument `backwards` is a boolean which is by default `False` meaning all the
events will be read forwards by default, so that events are returned in the
order they were committed, If `backwards` is `True`, all the events will be read
backwards, so that events are returned in reverse order.

The argument `limit` is an integer which limits the number of events that will
be returned.

Please note, if `backwards` is used in combination with `position`, the recorded
event at the given commit position will NOT be included. This differs from reading
events from a stream backwards from a stream position, when the recorded event at
the given stream position WILL be included.

Read recorded events in a stream from a particular position.

```python
events = list(client.read_all_events(position=commit_position1))

assert len(events) == 3

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 0
assert events[0].type == event1.type
assert events[0].data == event1.data

assert events[1].stream_name == stream_name1
assert events[1].stream_position == 1
assert events[1].type == event2.type
assert events[1].data == event2.data

assert events[2].stream_name == stream_name1
assert events[2].stream_position == 2
assert events[2].type == event3.type
assert events[2].data == event3.data
```

Read all the recorded events backwards from the end.

```python
events = list(client.read_all_events(backwards=True))

assert len(events) >= 3

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 2
assert events[0].type == event3.type
assert events[0].data == event3.data

assert events[1].stream_name == stream_name1
assert events[1].stream_position == 1
assert events[1].type == event2.type
assert events[1].data == event2.data

assert events[2].stream_name == stream_name1
assert events[2].stream_position == 0
assert events[2].type == event1.type
assert events[2].data == event1.data
```

Read a limited number of recorded events from a specific commit position.

```python
events = list(client.read_all_events(position=commit_position1, limit=1))

assert len(events) == 1

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 0
assert events[0].type == event1.type
assert events[0].data == event1.data
```

Read a limited number of recorded events backwards from the end.

```python
events = list(client.read_all_events(backwards=True, limit=1))

assert len(events) == 1

assert events[0].stream_name == stream_name1
assert events[0].stream_position == 2
assert events[0].type == event3.type
assert events[0].data == event3.data
```

### Stop EventStoreDB

Use Docker to stop and remove the EventStoreDB container.

    $ docker stop my-eventstoredb
	$ docker rm my-eventstoredb


## Developers

Clone the project repository, set up a virtual environment, and install
dependencies.

Use your IDE (e.g. PyCharm) to open the project repository. Create a
Poetry virtual environment, and then update packages.

    $ make update-packages

Alternatively, use the ``make install`` command to create a dedicated
Python virtual environment for this project.

    $ make install

The ``make install`` command uses the build tool Poetry to create a dedicated
Python virtual environment for this project, and installs popular development
dependencies such as Black, isort and pytest.

Add tests in `./tests`. Add code in `./esdbclient`.

Start EventStoreDB.

    $ make start-eventstoredb

Run tests.

    $ make test

Stop EventStoreDB.

    $ make stop-eventstoredb

Check the formatting of the code.

    $ make lint

Reformat the code.

    $ make fmt

Add dependencies in `pyproject.toml` and then update installed packages.

    $ make update-packages
