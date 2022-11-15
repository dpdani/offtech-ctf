# offtech-ctf

### Analyzer

From your local machine launch:

```
ssh -T <username>@users.isi.deterlab.net ssh -T <host>.ctf-resilient-g3.offtech "sudo tcpdump -s0 -U --immediate-mode -nn -i <interface> -w -" | python3 analyze_pcap.py
```

NB: requires `pyshark` and `flask` installed on your local machine
