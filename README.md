# OpenMaverick

## Cloning and working with Git
1. To begin, clone the repository using `git clone <URL>`. If you are using HTTPS this would look like `git clone https://github.com/Atjowt/openmav.git`.
2. Whenever you want to make some changes on your local machine, start by doing a `git pull --rebase` to avoid unnecessary merge conflicts later down the line.
3. Make sure to provide a reasonable commit message for your changes, see `git log` for a history of previous commits.
4. When you are done making your changes, first verify that nothing is seriously broken, and then push your changes with `git push`.

## Setting up and running the examples
FlightGear has an internal Property Tree containing all information about the current state; position, orientation, weather conditions, etc. The program exposes a few different methods for communicating with the program, of which we use TCP and UDP sockets. There is also support for HTTP: by running FlightGear with `fgfs --httpd=5000` you can go to `localhost:5000` in your web browser, which will take you to the builtin FlightGear web API. Here you can go to to Simulator > Properties to inspect the property tree and even change some values.

As mentioned earlier, OpenMav uses sockets to communicate. FlightGear has a "general" protocol which lets you specify your own datadata  protocol through an XML file. OpenMav defines its own protocol in the file `protocol/openmav.xml`, which **must be copied locally** to `$FG_ROOT/Protocol` for FlightGear to recognize it on launch.
With the protocol installed, you should be able to run the examples `launch_example.py` and `connect_example.py`.
