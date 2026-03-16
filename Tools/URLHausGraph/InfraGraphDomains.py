import asyncio, aiohttp, csv, ipaddress, tldextract, textwrap
from urllib.parse import urlparse
from collections import defaultdict
from pyvis.network import Network
from tabulate import tabulate

URLHAUS="https://urlhaus.abuse.ch/downloads/csv_recent/"
ASN_FILE="ip2asn-v4.tsv"
MAX_DOMAINS=400
CONCURRENCY=100

ranges=[]


def load_asn():
    with open(ASN_FILE,encoding="utf-8") as f:
        for line in f:
            p=line.strip().split("\t")
            if len(p)<5:
                continue
            try:
                start=int(ipaddress.IPv4Address(p[0]))
                end=int(ipaddress.IPv4Address(p[1]))
                asn=int(p[2])
                name=p[4]
                ranges.append((start,end,asn,name))
            except:
                pass


def lookup_asn(ip):
    i=int(ipaddress.IPv4Address(ip))
    for s,e,a,n in ranges:
        if s<=i<=e:
            return a,n
    return None,None


def normalize(host):
    ext=tldextract.extract(host)
    return f"{ext.domain}.{ext.suffix}" if ext.suffix else None


def is_ip(h):
    try:
        ipaddress.ip_address(h)
        return True
    except:
        return False


async def fetch_domains():

    async with aiohttp.ClientSession() as s:
        async with s.get(URLHAUS) as r:
            text=await r.text()

    reader=csv.reader(text.splitlines())
    domains=set()

    for row in reader:

        if not row or row[0].startswith("#"):
            continue

        try:

            host=urlparse(row[2]).netloc.split(":")[0]

            if is_ip(host):
                continue

            dom=normalize(host)

            if dom:
                domains.add(dom)

        except:
            pass

    return list(domains)[:MAX_DOMAINS]


async def resolve(domain):

    loop=asyncio.get_event_loop()

    try:

        res=await asyncio.wait_for(loop.getaddrinfo(domain,None),3)

        ip=res[0][4][0]

        if ":" in ip:
            return None

        return ip

    except:
        return None


async def process(domains):

    sem=asyncio.Semaphore(CONCURRENCY)

    results=[]

    async def worker(d):

        async with sem:

            ip=await resolve(d)

            if not ip:
                return

            asn,name=lookup_asn(ip)

            results.append((d,ip,asn,name))

    await asyncio.gather(*(worker(x) for x in domains))

    return results


def terminal_output(data):

    rows=[[d,ip,f"AS{a}" if a else "",n or ""] for d,ip,a,n in data]

    print("\nDomain Infrastructure\n")

    print(tabulate(rows,
        headers=["Domain","IP","ASN","Network"],
        tablefmt="simple"))

    asn_domains=defaultdict(list)
    ip_clusters=defaultdict(list)
    asn_names={}

    for d,ip,a,n in data:

        ip_clusters[ip].append(d)

        if a:
            asn_domains[a].append(d)
            asn_names[a]=n

    asn_rows=[]

    for asn,domains in sorted(asn_domains.items(),key=lambda x:len(x[1]),reverse=True):

        domains=sorted(domains)

        domlist=textwrap.fill(", ".join(domains),80)

        asn_rows.append([
            f"AS{asn}",
            asn_names[asn],
            len(domains),
            domlist
        ])

    print("\nASN Infrastructure Clusters\n")

    print(tabulate(
        asn_rows,
        headers=["ASN","Network","Domains","Domain List"],
        tablefmt="simple"
    ))

    reuse=[]

    for ip,domains in sorted(ip_clusters.items(),key=lambda x:len(x[1]),reverse=True):

        if len(domains)>1:

            domains=sorted(domains)

            domlist=textwrap.fill(", ".join(domains),80)

            reuse.append([
                ip,
                len(domains),
                domlist
            ])

    if reuse:

        print("\nShared Infrastructure\n")

        print(tabulate(
            reuse,
            headers=["IP","Domain Count","Domains"],
            tablefmt="simple"
        ))


def export_graph(data):

    ip_clusters=defaultdict(list)
    asn_map={}
    domain_set=set()
    ip_set=set()
    asn_domains=defaultdict(list)
    asn_names={}
    asn_ip_map=defaultdict(lambda:defaultdict(list))

    for d,ip,a,n in data:

        domain_set.add(d)
        ip_set.add(ip)

        ip_clusters[ip].append(d)

        if a:
            asn_map[ip]=(a,n)
            asn_domains[a].append(d)
            asn_names[a]=n
            asn_ip_map[a][ip].append(d)

    net=Network(
        height="100%",
        width="100%",
        bgcolor="#0f172a",
        font_color="#e2e8f0"
    )

    net.set_options("""
    {
      "physics": {
        "enabled": true,
        "forceAtlas2Based": {
          "gravitationalConstant": -150,
          "centralGravity": 0.01,
          "springLength": 180,
          "springConstant": 0.02,
          "avoidOverlap": 1
        },
        "solver": "forceAtlas2Based",
        "stabilization": { "iterations": 300 }
      }
    }
    """)

    for asn,domains in sorted(asn_domains.items(),key=lambda x:len(x[1]),reverse=True):

        tooltip="<br>".join(sorted(domains))

        net.add_node(
            f"asn:{asn}",
            label=f"AS{asn}\n{len(domains)} domains",
            title=tooltip,
            color="#22c55e",
            size=50
        )

    for ip,domains in sorted(ip_clusters.items(),key=lambda x:len(x[1]),reverse=True):

        domains=sorted(domains)

        tooltip=f"<b>{ip}</b><br><br>Domains Hosted:<br>"+"<br>".join(domains)

        net.add_node(
            f"ip:{ip}",
            label=f"{ip}\n{len(domains)}",
            title=tooltip,
            color="#38bdf8",
            size=30
        )

        if ip in asn_map:

            a,n=asn_map[ip]

            net.add_edge(
                f"ip:{ip}",
                f"asn:{a}",
                width=3,
                color="#94a3b8"
            )

        for d in domains:

            net.add_node(
                f"d:{d}",
                label=d,
                color="#fb7185",
                size=12
            )

            net.add_edge(
                f"d:{d}",
                f"ip:{ip}",
                width=1,
                color="#64748b"
            )

    net.write_html("graph.html")

    reuse_ips=[(ip,domains)
        for ip,domains in ip_clusters.items()
        if len(domains)>1]

    sidebar=f"""
<div class="sidebar">

<h1>Threat Infrastructure</h1>

<div class="metrics">

<div class="card">
<h3>Domains</h3>
<p>{len(domain_set)}</p>
</div>

<div class="card">
<h3>IPs</h3>
<p>{len(ip_set)}</p>
</div>

<div class="card">
<h3>ASNs</h3>
<p>{len(asn_domains)}</p>
</div>

</div>

<h2>ASN Clusters</h2>

<table class="tbl">
<tr><th>ASN</th><th>Count</th><th>Domains</th></tr>
"""

    for asn,domains in sorted(asn_domains.items(),key=lambda x:len(x[1]),reverse=True):

        domains=sorted(domains)

        sidebar+=f"<tr><td>AS{asn}</td><td>{len(domains)}</td><td>{'<br>'.join(domains)}</td></tr>"

    sidebar+="</table>"

    if reuse_ips:

        sidebar+="<h2>Shared Infrastructure</h2>"
        sidebar+="<table class='tbl'><tr><th>IP</th><th>Count</th><th>Domains</th></tr>"

        for ip,domains in sorted(reuse_ips,key=lambda x:len(x[1]),reverse=True):

            domains=sorted(domains)

            sidebar+=f"<tr><td>{ip}</td><td>{len(domains)}</td><td>{'<br>'.join(domains)}</td></tr>"

        sidebar+="</table>"

    sidebar+="<h2>ASN Infrastructure</h2>"

    for asn,ips in sorted(
        asn_ip_map.items(),
        key=lambda x:sum(len(v) for v in x[1].values()),
        reverse=True
    ):

        total_domains=sum(len(v) for v in ips.values())

        sidebar+=f"""
<details>
<summary><b>AS{asn}</b> — {total_domains} domains / {len(ips)} IPs</summary>
"""

        for ip,domains in sorted(ips.items(),key=lambda x:len(x[1]),reverse=True):

            domains=sorted(domains)

            sidebar+=f"""
<div class="ipblock">
<b>{ip}</b> ({len(domains)})
<div class="domlist">
{'<br>'.join(domains)}
</div>
</div>
"""

        sidebar+="</details>"

    sidebar+="</div>"

    css="""
<style>

body{
margin:0;
display:flex;
font-family:system-ui;
background:#0f172a;
color:#e2e8f0;
}

.sidebar{
width:380px;
padding:28px;
background:#020617;
border-right:1px solid #1e293b;
overflow:auto;
}

.sidebar h1{
margin-top:0;
font-size:22px;
}

.sidebar h2{
margin-top:30px;
font-size:16px;
border-bottom:1px solid #1e293b;
padding-bottom:6px;
}

.metrics{
display:grid;
grid-template-columns:1fr 1fr;
gap:10px;
margin-top:20px;
}

.card{
background:#020617;
border:1px solid #1e293b;
padding:14px;
border-radius:6px;
}

.card h3{
margin:0;
font-size:12px;
color:#94a3b8;
}

.card p{
margin:4px 0 0 0;
font-size:20px;
font-weight:600;
}

.tbl{
width:100%;
border-collapse:collapse;
margin-top:10px;
}

.tbl th{
text-align:left;
font-size:12px;
color:#94a3b8;
padding:6px;
border-bottom:1px solid #1e293b;
}

.tbl td{
padding:6px;
font-size:13px;
vertical-align:top;
}

details{
margin-top:10px;
border:1px solid #1e293b;
border-radius:6px;
padding:8px;
background:#020617;
}

summary{
cursor:pointer;
font-size:13px;
}

.ipblock{
margin-top:8px;
padding:6px;
border-left:2px solid #38bdf8;
font-size:12px;
}

.domlist{
margin-left:8px;
color:#94a3b8;
font-size:12px;
}

#mynetwork{
flex:1;
height:100vh;
}

</style>
"""

    with open("graph.html","r",encoding="utf-8") as f:
        html=f.read()

    html=html.replace("<body>",f"<body>{sidebar}")
    html=html.replace("</head>",f"{css}</head>")

    with open("graph.html","w",encoding="utf-8") as f:
        f.write(html)

    print("\nGraph exported: graph.html")


async def main():

    load_asn()

    domains=await fetch_domains()

    data=await process(domains)

    terminal_output(data)

    export_graph(data)


asyncio.run(main())