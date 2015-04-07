# Snort Docker Image

This is a Docker image with a ready to use Snort and PulledPork
install.  Just provide your oinkcode.

## Usage

### Download Some Rules

```
echo OINKCODE=<YOUR_OINKCODE> >> config
./launcher run /tools/update-rules
```

### Run Snort

```
./launcher run snort -c /etc/snort/snort.conf -i <interface>
```

The path to the snort.conf is the path inside the container rather
than on the host.

By default, the launcher script will start Docker with host network to
give Snort access to the host interfaces.


### Review The Logs

```
tail -f ./data/var/log/snort/alert
```

Note that the above command is run outside of the container. By
default, Snort will log to /data/var/log/snort, which is mapped into
the ./data directory on the host.

### Tune Your Rules with Pulled Pork

After you have run the container at least once, you will find the
basic set of Pulled Pork configuration files in ./data/etc.  Just edit
these files as you normally would, then run:

```
./launcher run /tools/update-rules
```

Then restart Snort.
