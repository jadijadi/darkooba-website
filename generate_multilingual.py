from pathlib import Path
import re
import shutil
import textwrap


ROOT = Path(__file__).resolve().parent
CONTENT_ROOT = ROOT / "content"
FA_ROOT = CONTENT_ROOT / "fa"
EN_ROOT = CONTENT_ROOT / "en"

SLUGS = [
    "about-us",
    "animals",
    "asb",
    "bahambesazim",
    "calendar",
    "contact",
    "dasht",
    "ghayegh",
    "jabekhiyal",
    "jorchin",
    "kajdar",
    "kamion",
    "miz",
    "products",
    "1khane",
    "workshops",
    "workshop-kid-and-city",
    "workshop-toys",
    "workshop-woodworking",
]


def parse_front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    title = ""
    if lines and lines[0].strip() == "---":
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        fm_lines = lines[1:end]
        body = "\n".join(lines[end + 1 :]).strip()
        for line in fm_lines:
            if line.startswith("title:"):
                title = line.split(":", 1)[1].strip().strip('"')
                break
    else:
        body = text.strip()
    return title, body


def relativize_internal_links(body: str) -> str:
    for slug in SLUGS:
        body = body.replace(f'href="/{slug}/"', f'href="../{slug}/"')
        body = body.replace(f"href='/{slug}/'", f"href='../{slug}/'")
    return body


def clean_fa_body(slug: str, body: str) -> str:
    body = relativize_internal_links(body)
    body = re.sub(r'<footer class="footer">.*?</footer>\s*', "", body, flags=re.S)
    if slug == "dasht":
        body = body.replace("بازی با <b></b> در اتاق انتظار پزشکان", "بازی با <b>دشت</b> در اتاق انتظار پزشکان")
    return body.strip() + "\n"


def write_page(lang_root: Path, slug: str, title: str, body: str, aliases=None):
    aliases = aliases or []
    page_dir = lang_root / slug
    page_dir.mkdir(parents=True, exist_ok=True)
    fm = ["---", f'title: "{title}"']
    if aliases:
        fm.append("aliases:")
        for alias in aliases:
            fm.append(f"  - {alias}")
    fm.append("---")
    content = "\n".join(fm) + "\n\n" + textwrap.dedent(body).strip() + "\n"
    (page_dir / "index.md").write_text(content, encoding="utf-8")


def write_home(lang_root: Path, title: str, aliases=None):
    aliases = aliases or []
    fm = ["---", f'title: "{title}"']
    if aliases:
        fm.append("aliases:")
        for alias in aliases:
            fm.append(f"  - {alias}")
    fm.append("---")
    (lang_root / "_index.md").write_text("\n".join(fm) + "\n", encoding="utf-8")


EN_PAGES = {
    "about-us": {
        "title": "About Us",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<img src="/images/about-us/darkooba-logo-full.png" class="darkooba-logo-full img-responsive">
<h3>Darkooba Toy Design and Making Group</h3>
<div class="videoWrapper">
<iframe src="http://www.aparat.com/video/video/embed/videohash/KUXez/vt/frame" allowFullScreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" height="360" width="640" ></iframe>
</div>
</br>
<p>In 2000, during a climb to Mount Azad Kuh, we met one another. We were so excited by every piece of wood and stone we saw that friendship was inevitable.</p>
<p>Very soon we opened a small woodworking studio together. It stood in the yard of an old garden and did not even have proper walls. Ignoring the winter cold, we spent long hours designing and making things simply because we loved it. At that time there were three of us. As life went on, our third friend moved to England and is now a design professor at Brunel University. Farzaneh went to the far western edge of the world and studied public-space architecture in Vancouver. She later worked in Canada and the United States on playgrounds and public spaces, and those experiences led her toward participatory design and working with teenagers. During those same years, Yasaman turned our woodshop into a home workshop and became a full-time teacher, creating creative lesson plans that introduced children of different ages to the arts and helped them believe in the abilities of their hands and minds.</p>
<p>In the winter of 2013, each of us sat down with a long list of wishes, dreams, skills, and possibilities, plus two cups of tea, and imagined a group that could help make “play for everyone” real. A group that designs and produces high-quality Iranian toys, creates special play tools and environments, and runs educational workshops. That is how <b>Darkooba</b> was born.</p>
<p>Watch the video above to get a closer sense of Darkooba’s philosophy and working environment.</p>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Darkooba</h3>
<br>
<h4>Yasaman Alishahi</h4>
<p>BSc in Mechanical Engineering | Sharif University</p>
<br>
<h4>Farzaneh Ghasemi</h4>
<p>BSc in Industrial Design | University of Tehran<br>
MA in Public Space Architecture | UBC</p>
<br>
</div>
</div>
<div class="col-sm-7">
<img src="/images/about-us/about-us.jpg" class="img-responsive">
</div>
</div>
</div>
</section>
""",
    },
    "animals": {
        "title": "Animals",
        "body": """
<div class="container">
<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-sm-4">
<div class="features-side-text">
<h3>Animals</h3>
<p>Sometimes a journey, a documentary, or an image leaves us enchanted by a giraffe, a whale, or a horse. Their grandeur stays in our minds for days. We make this collection in an effort to hold on to some of that beauty.</p>
</div>
</div>
<div class="col-sm-8">
<img src="/images/a1.jpg">
</div>
</div>
</section>

<section class="features u-img-responsive u-img-paddig u-img-border">
<div class="row">
<div class="col-sm-4">
<img src="/images/a4.jpg">
</div>
<div class="col-sm-4">
<img src="/images/a2.jpg">
</div>
<div class="col-sm-4">
<img src="/images/a3.jpg">
</div>
</div>
</section>
</div>
""",
    },
    "asb": {
        "title": "Horse",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Horse</h3>
<p>In <b>Let’s Build a Horse</b>, children receive all the parts they need to build a horse. The wood glue and sandpaper included in the package let them experience a real woodworking project. The illustrated guide helps them follow the steps, while still leaving them free to shape the process in their own way. In the end, they have a rocking horse they can enjoy again and again.</p>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-xs-4">
<img src="/images/build-toghether/horse/horse-01.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/horse/horse-03.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/horse/horse-02.jpg">
</div>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Specifications</h3>
<p><b>Package size:</b> a cylinder 8 cm in diameter and 14 cm high</p>
<p><b>Built horse size:</b> 11.5 × 5 × 15 cm</p>
<p><b>Horse weight:</b> 90 g</p>
<p><b>Age group:</b> recommended for ages 4 and up, though younger children who enjoy making things can build it with adult help or play with the finished toy.</p>
</div>
</div>
<div class="col-sm-7">
<div><img src="/images/build-toghether/horse/horse-04.jpg"></div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<h3 class="u-center-text">Other products in the <b>Let’s Build Together</b> collection</h3>
<div class="col-sm-4">
<div class="card">
<a href="../ghayegh/" class="u-no-decoration">
<img src="/images/build-toghether/boat.jpg">
<h4 class="card-title">Boat</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../kamion/" class="u-no-decoration">
<img src="/images/build-toghether/car.jpg">
<h4 class="card-title">Truck</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../miz/" class="u-no-decoration">
<img src="/images/build-toghether/table.jpg">
<h4 class="card-title">Table and Chairs</h4>
</a>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "bahambesazim": {
        "title": "Let's Build Together",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Let’s Build Together</h3>
<p><b>Let’s Build Together</b> is for children who do not want to be only users of their toys. It is for those who want to take part in making them, to be responsible for part of the process, to paint them as they like, to add personal touches, and to make their toys truly their own.</p>
<p><b>Let’s Build Together</b> is a collection. So far it includes a rocking horse, a truck, a boat, and a small table-and-chairs set, and more packages are on the way.</p>
</div>
</div>
</div>
</section>

<section class="u-img-responsive u-img-border u-img-paddig">
<div class="container">
<div class="row">
<div class="box col-sm-6">
<a href="../asb/">
<div class="product-name-cnt">Horse</div>
<img src="/images/build-toghether/horse.jpg">
</a>
</div>
<div class="box col-sm-6">
<a href="../kamion/">
<div class="product-name-cnt">Truck</div>
<img src="/images/build-toghether/car.jpg">
</a>
</div>
<div class="box col-sm-6">
<a href="../miz/">
<div class="product-name-cnt">Table and Chairs</div>
<img src="/images/build-toghether/table.jpg">
</a>
</div>
<div class="box col-sm-6">
<a href="../ghayegh/">
<div class="product-name-cnt">Boat</div>
<img src="/images/build-toghether/boat.jpg">
</a>
</div>
</div>
</div>
</section>

<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6">
<h4>Physical Features</h4>
<p>This collection is made from natural pine wood, not MDF, plywood, or composite materials.</p>
<p>It uses untreated pine so children can paint it any way they like.</p>
</div>
<div class="col-sm-6">
<h4>Why build together?</h4>
<p>Making this collection helps strengthen children’s hands-on skills.</p>
<p>They practice reading plans and following a visual guide.</p>
<p>They experience completing a project and solving problems.</p>
<p>They come up with ideas to personalize their tools and toys.</p>
<p>As a result, their confidence in their abilities grows.</p>
<p>Playing with wood as a natural material also helps develop children’s senses.</p>
</div>
</div>
</div>
</section>
""",
    },
    "calendar": {
        "title": "Calendar",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Calendar</h3>
<p>We wanted a calendar that felt like our own world, something wooden that could also awaken the imagination. A calendar with pieces that could be moved and added to. A calendar that could be kept from one year to the next, growing into a more beautiful scene over time. A calendar that could serve other purposes too, like becoming a photo stand.</p>
</div>
</div>
</div>
</section>

<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-12">
<div class="calender-cnt">
<div class="js-calender-slide calender-slide" dir="ltr">
<div><img src="/images/calender/calender-01.jpg"></div>
<div><img src="/images/calender/calender-02.jpg"></div>
<div><img src="/images/calender/calender-03.jpg"></div>
<div><img src="/images/calender/calender-04.jpg"></div>
<div><img src="/images/calender/calender-05.jpg"></div>
<div><img src="/images/calender/calender-06.jpg"></div>
</div>
<img class="calender-fg" src="/images/calender-fg.png">
</div>
</div>
</div>
</div>
</section>

<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<p>For the 1393 calendar we illustrated skies to complete the scene of the house and the trees. For the 1394 calendar we built wooden models of different Iranian landscapes and placed them behind the calendar: small images inspired by our journeys through unforgettable places in Iran.</p>
</div>
</div>
</div>
</section>
""",
    },
    "contact": {
        "title": "Contact",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-md-8 col-md-offset-2 col-sm-10 col-sm-offset-1">
<div class="contact-info">
<br>
<p>Send your questions about Darkooba’s products and workshops to the email address below. We will respond as soon as possible.</p>
<h3><a href="mailto:info@darkooba.com">info@darkooba.com</a></h3>
<br>
<p>You can also reach us during working hours at the phone number below.</p>
<h3 dir="ltr"><a href="tel:+982122704519">021-22704519</a></h3>
<br>
<p>This version of the site is built statically with Hugo, so the old contact form has been removed and communication now happens through email and phone.</p>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "dasht": {
        "title": "Landscape",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Landscape</h3>
<p>Every now and then we leave the city and head toward wide, generous plains. We rest beside them for an hour or a day, walk among them, sit under leafy trees, and gaze at cottages, colorful hills, flocks of sheep, and their shepherd. <b>Landscape</b> is our way of rebuilding these scenes inside urban life, exactly as we would like them to be.</p>
</div>
</div>
</div>
</section>

<div class="features lanscape-panorama">
<div class="container-fluid">
<div class="row">
<img src="/images/landscape/landscape-panorama.jpg" class="u-img-full-width">
</div>
</div>
</div>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>A setting for children’s storytelling</h3>
<p><b>Landscape</b> gives children a stage for storytelling. They can combine its pieces with their own toys, build the land they want, and use it to invent new stories.</p>
</div>
</div>
<div class="col-sm-7">
<div class="js-slider-dotted" dir="ltr">
<div><img src="/images/landscape/landscape-kids-1.jpg"></div>
<div><img src="/images/landscape/landscape-kids-2.jpg"></div>
<div><img src="/images/landscape/landscape-kids-3.jpg"></div>
<div><img src="/images/landscape/landscape-kids-4.jpg"></div>
</div>
</div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-5 col-sm-push-7">
<div class="features-side-text">
<h3>Calm and renewal in the workplace</h3>
<p>Between demanding hours of work and concentration, we can turn to the <b>Landscape</b> table, move the pieces around, arrange a favorite scene, travel for a moment, and return to work with more calm.</p>
<p>The <b>Landscape</b> table shown here was made for <b>Cafe Bazaar</b> and is installed at the company’s office.</p>
</div>
</div>
<div class="col-sm-7 col-sm-pull-5">
<div class="js-slider-dotted" dir="ltr">
<div><img src="/images/landscape/landscape-work-1.jpg"></div>
<div><img src="/images/landscape/landscape-work-2.jpg"></div>
<div><img src="/images/landscape/landscape-work-3.jpg"></div>
<div><img src="/images/landscape/landscape-work-4.jpg"></div>
<div><img src="/images/landscape/landscape-work-5.jpg"></div>
<div><img src="/images/landscape/landscape-work-6.jpg"></div>
<div><img src="/images/landscape/landscape-work-7.jpg"></div>
<div><img src="/images/landscape/landscape-work-8.jpg"></div>
</div>
</div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Making waiting time shorter and gentler</h3>
<p>Waiting hours in medical centers can be stressful for both children and adults. Playing with <b>Landscape</b> in a doctor’s waiting room makes that time shorter and more pleasant.</p>
<p>The <b>Landscape</b> table shown here was made for <b>Dr. Parisa Aref</b>, a pediatric dentist, and is installed in her office.</p>
</div>
</div>
<div class="col-sm-7">
<div class="js-slider-dotted" dir="ltr">
<div><img src="/images/landscape/landscape-sneeze-time-1.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-2.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-3.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-4.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-5.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-6.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-7.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-8.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-9.jpg"></div>
<div><img src="/images/landscape/landscape-sneeze-time-10.jpg"></div>
</div>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "ghayegh": {
        "title": "Boat",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Boat</h3>
<p>In <b>Let’s Build a Boat</b>, children receive all the parts needed to build a boat. The wood glue and sandpaper in the package let them experience a real woodworking project. The illustrated guide helps them follow the process, while still giving them freedom at every step to predict and shape the making process in their own way. In the end they have a boat powered by a rubber band that moves across water, a toy to enjoy again and again through a warm summer.</p>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-xs-4">
<img src="/images/build-toghether/boat/boat-01.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/boat/boat-02.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/boat/boat-03.jpg">
</div>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Specifications</h3>
<p><b>Package size:</b> a cylinder 8 cm in diameter and 14 cm high</p>
<p><b>Built boat size:</b> 14.5 × 7 × 5 cm</p>
<p><b>Boat weight:</b> 90 g</p>
<p><b>Age group:</b> recommended for ages 4 and up, though younger children who enjoy making things can build it with adult help or play with the finished toy.</p>
</div>
</div>
<div class="col-sm-7">
<div class="js-slider-dotted" dir="ltr">
<div><img src="/images/build-toghether/boat/boat-04.jpg"></div>
<div><img src="/images/build-toghether/boat/boat-05.jpg"></div>
<div><img src="/images/build-toghether/boat/boat-06.jpg"></div>
</div>
</div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<h3 class="u-center-text">Other products in the <b>Let’s Build Together</b> collection</h3>
<div class="col-sm-4">
<div class="card">
<a href="../asb/" class="u-no-decoration">
<img src="/images/build-toghether/horse.jpg">
<h4 class="card-title">Horse</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../kamion/" class="u-no-decoration">
<img src="/images/build-toghether/car.jpg">
<h4 class="card-title">Truck</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../miz/" class="u-no-decoration">
<img src="/images/build-toghether/table.jpg">
<h4 class="card-title">Table and Chairs</h4>
</a>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "jabekhiyal": {
        "title": "Boxes of Imagination",
        "body": """
<div class="container">
<section class="features">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Boxes of Imagination</h3>
<p>There are places and scenes that feel calming and full of memory for us, spaces we can hardly reach in the rush of everyday urban life. In <b>Boxes of Imagination</b> we have pictured fragments of that lost sense of peace, so they can return it to us for a few moments. Whether the box sits on a shelf at home or travels with you in your backpack, you can open it from time to time and take refuge in its scene.</p>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-sm-4">
<div class="features-side-text">
<h3>Sea</h3>
<p>The endless blue of the sea, and sails of many colors dancing in the wind.</p>
</div>
</div>
<div class="col-sm-8">
<img src="/images/d1.jpg">
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-sm-4 col-sm-push-8">
<div class="features-side-text">
<h3>Old Square</h3>
<p>A fresh morning in one corner of an old clock square in a desert town. From far away, the bell of a bicycle can be heard.</p>
</div>
</div>
<div class="col-sm-8 col-sm-pull-4">
<img src="/images/d2.jpg">
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-sm-4">
<div class="features-side-text">
<h3>Images</h3>
<p>Every image is a story. A box full of stories.</p>
</div>
</div>
<div class="col-sm-8">
<img src="/images/d3.jpg">
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-sm-4 col-sm-push-8">
<div class="features-side-text">
<h3>Fire</h3>
<p>Nomad, where is your night dance beside the fire?</p>
</div>
</div>
<div class="col-sm-8 col-sm-pull-4">
<img src="/images/d4.jpg">
</div>
</div>
</section>
</div>
""",
    },
    "jorchin": {
        "title": "Jorchin",
        "body": """
<div class="container">
<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-md-4">
<div class="features-side-text">
<h3>Jorchin</h3>
<ul>
<li>Playing with <b>Jorchin</b> is an exercise in hand-eye coordination.</li>
<li><b>Jorchin</b> gives children a flexible set of colorful wooden blocks they can assign different roles to in their stories and imaginative play.</li>
</ul>
</div>
</div>
<div class="col-md-8">
<img src="/images/puzzle/puzzle-2.jpg">
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-sm-4">
<img src="/images/puzzle/puzzle-1.jpg">
</div>
<div class="col-sm-8">
<img src="/images/puzzle/puzzle-3.jpg">
</div>
</div>
</section>
</div>
""",
    },
    "kajdar": {
        "title": "Balance Blocks",
        "body": """
<div class="container">
<section class="features">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h2>Balance Blocks</h2>
<p>Stacking stones to create balanced forms is a play pattern that has been around for a very long time. Some people turned it into a game with rules, like seven stones. Others, like the Inuit in North America, used it to create decorative balancing forms called inukshuks.</p>
<p>Inspired by all of these, we created <b>Balance Blocks</b>.</p>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="row">
<div class="col-xs-4">
<img src="/images/girl-1.jpg">
</div>
<div class="col-xs-4">
<img src="/images/girl-2.jpg">
</div>
<div class="col-xs-4">
<img src="/images/girl-3.jpg">
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="row">
<div class="col-sm-4 col-sm-push-8">
<div class="features-side-text">
<h4>For children and adults</h4>
<p><b>Balance Blocks</b> is a physical toy for children that helps develop fine motor skills. Building balanced forms with it gives children a hands-on understanding of gravity, weight, and equilibrium.</p>
<p>For adults it can be both a quiet focus toy that helps them relax alone and a social toy for gatherings. A pile of colorful wooden pieces that is exciting to stack together and joyful to hear collapse.</p>
</div>
</div>
<div class="col-sm-8 col-sm-pull-4">
<img src="/images/k1.jpg">
</div>
</div>
</section>

<section class="features" dir="ltr">
<div class="js-slider-dotted slider-center">
<div><img src="/images/kajdar-mariz/kajdar-mariz-slide-01.jpg"></div>
<div><img src="/images/kajdar-mariz/kajdar-mariz-slide-02.jpg"></div>
</div>
</section>
</div>
""",
    },
    "kamion": {
        "title": "Truck",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Truck</h3>
<p>In <b>Let’s Build a Truck</b>, children receive all the parts needed to build a truck. The wood glue and sandpaper in the package let them experience a woodworking project. The illustrated guide helps them follow the steps, while still leaving freedom at every stage to imagine and carry out the making process in their own way. In the end they have a truck with rolling wheels and a dumping bed that moves up and down, a toy they can keep enjoying long after building it.</p>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-xs-4">
<img src="/images/build-toghether/car/car-01.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/car/car-02.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/car/car-03.jpg">
</div>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Specifications</h3>
<p><b>Package size:</b> a cylinder 8 cm in diameter and 14 cm high</p>
<p><b>Built truck size:</b> 12.5 × 9 × 7.5 cm</p>
<p><b>Truck weight:</b> 120 g</p>
<p><b>Age group:</b> recommended for ages 4 and up, though younger children who enjoy making things can build it with adult help or play with the finished toy.</p>
</div>
</div>
<div class="col-sm-7">
<div class="js-slider-dotted" dir="ltr">
<div><img src="/images/build-toghether/car/car-04.jpg"></div>
<div><img src="/images/build-toghether/car/car-05.jpg"></div>
</div>
</div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<h3 class="u-center-text">Other products in the <b>Let’s Build Together</b> collection</h3>
<div class="col-sm-4">
<div class="card">
<a href="../asb/" class="u-no-decoration">
<img src="/images/build-toghether/horse.jpg">
<h4 class="card-title">Horse</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../ghayegh/" class="u-no-decoration">
<img src="/images/build-toghether/boat.jpg">
<h4 class="card-title">Boat</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../miz/" class="u-no-decoration">
<img src="/images/build-toghether/table.jpg">
<h4 class="card-title">Table and Chairs</h4>
</a>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "miz": {
        "title": "Table and Chairs",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Table and Chairs</h3>
<p>In <b>Let’s Build a Table and Chairs</b>, children receive all the parts needed to make one table and three chairs. The wood glue and sandpaper in the package let them experience a woodworking project. The illustrated guide helps them follow the steps, while still giving them freedom at every stage to imagine and carry out the making process in their own way. In the end they can add fabric or paper details to complete the set and enjoy using it in their stories and imaginative play.</p>
</div>
</div>
</div>
</section>

<!-- <section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-xs-4">
<img src="/images/build-toghether/table/table-01.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/table/table-02.jpg">
</div>
<div class="col-xs-4">
<img src="/images/build-toghether/table/table-03.jpg">
</div>
</div>
</div>
</section> -->

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Specifications</h3>
<p>Because natural branches are used in this set, each table-and-chairs kit has slightly different dimensions.</p>
<p><b>Approximate size:</b> the approximate diameter of the table and chairs is 13 cm.</p>
<p><b>Age group:</b> recommended for ages 3 and up, though younger children who enjoy making things can build it with adult help or play with the finished toy.</p>
</div>
</div>
<div class="col-sm-7">
<div class="js-slider-dotted" dir="ltr">
<div><img src="/images/build-toghether/table/table-01.jpg"></div>
<!-- <div><img src="/images/build-toghether/table/table-05.jpg"></div> -->
</div>
</div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<h3 class="u-center-text">Other products in the <b>Let’s Build Together</b> collection</h3>
<div class="col-sm-4">
<div class="card">
<a href="../asb/" class="u-no-decoration">
<img src="/images/build-toghether/horse.jpg">
<h4 class="card-title">Horse</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../ghayegh/" class="u-no-decoration">
<img src="/images/build-toghether/boat.jpg">
<h4 class="card-title">Boat</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../kamion/" class="u-no-decoration">
<img src="/images/build-toghether/car.jpg">
<h4 class="card-title">Truck</h4>
</a>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "products": {
        "title": "Products",
        "body": """
<div class="products">
<div class="container">
<div class="row">
<div class="box col-xs-6 col-sm-3">
<a href="../kajdar/">
<div class="product-name-cnt">Balance Blocks</div>
<div class="height-2 img-fill-box unstable"></div>
</a>
</div>
<div class="box col-xs-6 col-sm-6">
<a href="../1khane/">
<div class="product-name-cnt">One House, A Hundred Stories</div>
<div class="height-1 img-fill-box iranianhome"></div>
</a>
</div>
<div class="box col-xs-6 col-sm-3">
<a href="../jabekhiyal/">
<div class="product-name-cnt">Boxes of Imagination</div>
<div class="height-1 img-fill-box dreambox"></div>
</a>
</div>
<div class="box col-xs-12 col-sm-9">
<a href="../dasht/">
<div class="product-name-cnt">Landscape</div>
<div class="height-1 img-fill-box landscape"></div>
</a>
</div>
</div>

<div class="row">
<div class="box col-xs-12 col-sm-6">
<a href="../bahambesazim/">
<div class="product-name-cnt">Let’s Build Together</div>
<div class="height-2 img-fill-box buildtogether"></div>
</a>
</div>
<div class="box col-xs-6 col-sm-3">
<a href="../jorchin/">
<div class="product-name-cnt">Jorchin</div>
<div class="height-1 img-fill-box puzzle"></div>
</a>
</div>
<div class="box col-xs-6 col-sm-3">
<a href="../animals/">
<div class="product-name-cnt">Animals</div>
<div class="height-1 img-fill-box animal"></div>
</a>
</div>
<div class="box col-xs-12 col-sm-6">
<a href="../calendar/">
<div class="product-name-cnt">Calendar</div>
<div class="height-1 img-fill-box calender"></div>
</a>
</div>
</div>
</div>
</div>
""",
    },
    "1khane": {
        "title": "One House, A Hundred Stories",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>One House, A Hundred Stories</h3>
<p><b>One House, A Hundred Stories</b> is a dollhouse inspired by Iranian architecture. It gives children a space to create their stories inside an Iranian house and, indirectly, to become familiar with and fond of fading layers of Iranian identity. The movable parts of <b>One House, A Hundred Stories</b> allow children to create different arrangements for a single house or even an entire neighborhood. Elements such as a pool, a cat, a tree, and stairways help children think about richer and more detailed stories and strengthen their language and storytelling skills.</p>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-xs-4">
<img src="/images/home/home-cover-1.jpg">
</div>
<div class="col-xs-4">
<img src="/images/home/home-cover-2.jpg">
</div>
<div class="col-xs-4">
<img src="/images/home/home-cover-3.jpg">
</div>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-4">
<div class="features-side-text">
<p>This toy includes a three-door room, two rectangular rooms, one entry space, 8 outer walls, a shared courtyard cloth, three stairways, one pool, two people, one tree, four garden beds, and one cat. Children can arrange these pieces in different ways to create one house, several houses, or a small neighborhood.</p>
</div>
</div>
<div class="col-sm-8">
<div><img src="/images/home/home-1.jpg"></div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-4">
<div class="features-side-text">
<h4>For children today</h4>
<p>This toy can become a meeting point between classic games such as playing house and contemporary digital tools. Ehsan Ahmadi, age 8, made the stop-motion animation opposite entirely on his own and in less than a few hours using this house.</p>
</div>
</div>
<div class="col-sm-8">
<div class="videoWrapper">
<iframe src="http://www.aparat.com/video/video/embed/videohash/YRDB4/vt/frame" allowFullScreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" height="360" width="640" ></iframe>
</div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive u-img-border">
<div class="container">
<div class="row">
<div class="col-sm-4">
<div class="features-side-text">
<h4>Children at play with One House, A Hundred Stories</h4>
<p>You can see some of the details of this dollhouse and the variety of spaces it creates for children’s play in the video opposite.</p>
</div>
</div>
<div class="col-sm-8">
<div class="videoWrapper">
<iframe src="http://www.aparat.com/video/video/embed/videohash/wlfrQ/vt/frame" allowFullScreen="true" webkitallowfullscreen="true" mozallowfullscreen="true" height="360" width="640" ></iframe>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "workshops": {
        "title": "Workshops",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Darkooba Workshops</h3>
<p>The main goal of our workshops is to strengthen children’s manual and mental abilities. We want them to make what they love and to know that they can.</p>
<p>For younger children we place making and construction inside a world of stories so the process is more exciting to follow. For older children we connect building with understanding a problem, identifying needs, designing, and evaluating.</p>
<p>In these workshops, not only the final objects but also the process itself is important and carefully designed.</p>
</div>
</div>
</div>
</section>

<section class="products u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-4">
<div class="card">
<a href="../workshop-kid-and-city/" class="u-no-decoration">
<img src="/images/workshops/kid and city/kid-city-cover.jpg">
<h4 class="card-title">Kids and the City Workshop</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../workshop-woodworking/" class="u-no-decoration">
<img src="/images/workshops/choob/choob-cover.jpg">
<h4 class="card-title">Wood Workshop</h4>
</a>
</div>
</div>
<div class="col-sm-4">
<div class="card">
<a href="../workshop-toys/" class="u-no-decoration">
<img src="/images/workshops/toys/toys-cover.jpg">
<h4 class="card-title">Toy-Making Workshop</h4>
</a>
</div>
</div>
</div>
</div>
</section>
""",
    },
    "workshop-kid-and-city": {
        "title": "Kids and the City Workshop",
        "body": """
<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Kids and the City Workshop</h3>
<p>The goal of this workshop series is to increase children’s attention to and awareness of topics connected to life in the city. During the workshops, children enter an empty city through a story and gradually build it using semi-prepared materials, guided by their needs and interests.</p>

<p>Each session focuses on one urban topic, and through the process of building the city, children become familiar with their urban rights and responsibilities through child-centered methods.</p>

<p>These workshops improve children’s hands-on skills and ability to make things, give them the experience of following a project through several sessions, help them practice teamwork, and increase their self-confidence.</p>
</div>
</div>
<div class="col-sm-7">
<div><img src="/images/workshops/kid and city/kid-city-cover.jpg"></div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h4>Workshop topics</h4>
<ul>
<li>Learning about public transportation in the city, how to use it, the ethics of using it, different kinds of streets and urban passages, and a number of transportation rules related to children</li>
<li>Getting to know buildings, their functions, their parts, and the ethics of being neighbors</li>
<li>Learning about urban green space, the benefits of trees in the city, the plane tree as a native tree of Tehran, and the ethics of living alongside urban animals</li>
<li>Getting to know urban furniture and how to use it responsibly</li>
</ul>
<p>This workshop was commissioned by the <b>Social Deputy of District 7 of Tehran Municipality</b> and carried out in cooperation with the <b>Insan Shahr Institute</b> in the district’s toy houses over an eight-month period.</p>
</div>
</div>
<div class="col-sm-7">
<div><img src="/images/workshops/kid and city/kid-city-1.jpg"></div>
</div>
</div>
</div>
</section>

<section class="features slider-center slider-landscape" dir="ltr">
<div class="js-slider-landscape slider-images">
<div><img src="/images/workshops/kid and city/kid-city-slide-01.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-02.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-03.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-04.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-05.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-06.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-07.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-08.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-09.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-10.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-11.jpg"></div>
</div>

<div class="js-slider-landscape-nav slider-navbar">
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-01.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-02.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-03.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-04.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-05.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-06.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-07.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-08.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-09.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-10.jpg"></div>
<div><img src="/images/workshops/kid and city/kid-city-slide-nav-11.jpg"></div>
</div>
</section>
""",
    },
    "workshop-toys": {
        "title": "Toy-Making Workshop",
        "body": """
<section class="features">
<div class="container">
<div class="row">
<div class="col-sm-6 col-sm-offset-3 product-intro-text">
<h3>Toy-Making Workshop</h3>
<p>Toys are one of the most beloved subjects for children, which makes them a very good doorway to indirect learning.</p>
<p>In this workshop, children not only become familiar with one making technique, but also build a usable toy of their own.</p>
<p>By making their own toys, children learn that they too can take action to bring their wishes to life.</p>
<p>These workshops have been held at the <b>Museum of Dolls and Culture</b> in Tehran and, in cooperation with the <b>Children’s Book Council</b>, in <b>Ali Akbar village in Sistan and Baluchestan Province</b>.</p>
</div>
</div>
</div>
</section>

<section class="features" dir="ltr">

<div class="slider-for">
<div><img src="/images/workshops/toys/toys-slide-01.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-02.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-03.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-04.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-05.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-06.jpg"></div>
</div>

<div class="slider-nav">
<div><img src="/images/workshops/toys/toys-slide-nav-01.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-nav-02.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-nav-03.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-nav-04.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-nav-05.jpg"></div>
<div><img src="/images/workshops/toys/toys-slide-nav-06.jpg"></div>
</div>

</section>
""",
    },
    "workshop-woodworking": {
        "title": "Wood Workshop",
        "body": """
<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h3>Wood Workshop</h3>
<p>In the <b>introductory wood workshop</b>, children learn basic woodworking skills, become familiar with several kinds of wood and their characteristics, and experience all of this within a story-based setting. In the advanced wood workshop, they learn more complex making skills and experience the full process of designing and building a product.</p>
</div>
</div>
<div class="col-sm-7">
<div><img src="/images/workshops/choob/choob-cover.jpg"></div>
</div>
</div>
</div>
</section>

<section class="features u-img-responsive">
<div class="container">
<div class="row">
<div class="col-sm-5">
<div class="features-side-text">
<h4>Workshop topics</h4>
<ul>
<li>Getting to know several kinds of wood and their properties</li>
<li>Becoming familiar with woodworking and making skills</li>
<li>Practicing problem-solving and completing projects</li>
<li>Practicing a few methods of group voting and reaching collective agreement</li>
<li>Learning basic schematic plan reading</li>
</ul>
<p>These workshops have so far been held at <b>Farzanegan Middle School, Raha Learning House, and Mehr Bam Educational Institute</b>.</p>
</div>
</div>
<div class="col-sm-7">
<div><img src="/images/workshops/choob/choob-1.jpg"></div>
</div>
</div>
</div>
</section>

<section class="features" dir="ltr">
<div class="slider-for">
<div><img src="/images/workshops/choob/choob-slide-01.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-02.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-03.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-04.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-05.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-06.jpg"></div>
</div>

<div class="slider-nav slider-navbar">
<div><img src="/images/workshops/choob/choob-slide-nav-01.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-nav-02.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-nav-03.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-nav-04.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-nav-05.jpg"></div>
<div><img src="/images/workshops/choob/choob-slide-nav-06.jpg"></div>
</div>
</section>
""",
    },
}


def main():
    for lang_root in [FA_ROOT, EN_ROOT]:
        if lang_root.exists():
            shutil.rmtree(lang_root)
        lang_root.mkdir(parents=True, exist_ok=True)

    write_home(FA_ROOT, "دارکوبا", aliases=["/fa/home/"])
    for slug in SLUGS:
        src = CONTENT_ROOT / slug / "index.md"
        title, body = parse_front_matter(src)
        write_page(FA_ROOT, slug, title, clean_fa_body(slug, body))

    write_home(EN_ROOT, "Darkooba", aliases=["/home/"])
    for slug, data in EN_PAGES.items():
        write_page(EN_ROOT, slug, data["title"], data["body"])


if __name__ == "__main__":
    main()
