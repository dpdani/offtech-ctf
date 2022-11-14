# offtech-ctf

### Analyzer

First run the `./capture.sh <host>` script in the control server.

Then from your local machine launch:

```
ssh -T <username>@users.isi.deterlab.net ssh -T <host>.ctf-resilient-g3.offtech "tail -f -n +1 ~/offtech-ctf/blue/pcap.pcap" | python3 analyze_pcap.py
```

NB: requires `pyshark` and `flask` installed on your local machine
