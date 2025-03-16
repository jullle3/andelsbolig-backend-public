# andelsbolig-backend
For frontend, se:
https://jullle3.github.io/andelsbolig-frontend

# Deploy dev
Fra terminal
gcloud app deploy app.yaml --version=2 --quiet

# V 1.0.0
- Lav scraper som indsamler andelsboliger fra dba, boliga, bolighed, andelsboligforeninger, facebook, instagram, twitter, linkedin, og andre sider
Scrape fra:
  - boliga
  - Boligsiden
  - dba
  - facebook? Har set at POST mod https://www.facebook.com/api/graphql/ kan finde andelsboliger
Måske burde jeg også manuelt indtaste andelsboliger på siden fra facebook?
- Overvej hvordan køber skal kontakte sælger. Skal det være som boligportalen, skal vi have en chat funktion eller skal de selv tage kontakt via sms/mail?
- Rework markers så de ligner de cards vi viser i home. Måske er der også brug for clustering, desværre
- Hvordan håndterer jeg GDPR, og behøver jeg overhovedet?
- Hvordan håndterer jeg en subscription som bliver renewed hver måned?
- Smoketest/gennemgang af hele frontend, for at sikre 0 bugs og fin UX. Test fra dev, ikke lokalt
  Få hjælp til denne test af bekendte.
  Ændringer i query på forsiden skal automatisk sende ny søgning mod backend.
- Opsæt et prod miljø
- Når en annonce er oprettet, vis en besked "Oprettet" med et flot ikon. Evt hav link så brugeren kan gå til annoncen
- Lav beregning på hvor meget Cloud vil koste ved 1000 brugere
- Support for SMS notifikationer?
- Undersøg hvordan jeg undgår mails havner i spam (Den til Malte havnede ikke i spam! (tror jeg...))
- Hvordan monitor jeg setuppet? Hvordan ved jeg om det går ned? kan det autoheal? 
- Flot landingpage. Er det dog nødvendigt? Se landingpage billederne samt https://www.anotherauction.dk/ 
- En kort guide til køb og salg
- Overvej at simplificere card view i advertisement list, lidt som på boligportal
- Gennemgå login begrænsning med is_authorized og is_subscribed, især i agent.controller.py

# Lav backend
- Brugere skal kunne uploade plantegning, og andre relevante dokumenter på en advertisement
- Kan systemet selv gennemskue om en bolig er placeret øverst?
- Rework mail notification til at bruge Amazon Simple Email Service. Det er billigere og mere skalerbart end at sende mails fra gmail der har hard limit på 500 om dagen
- Lav "Tips når du vil sælge" side, Inkluder tips på hjemmesiden til hvordan man bedst sælger sin andelsbolig, hvordan man tager gode billeder osv.
- Man skal kunne "favorite" advertisements
- Hvordan håndteres integration & versionering op mod stripe, gcloud, chatGPT? Vi skal nødigt have det breaker pludselig https://stripe.com/docs/api/versioning
- AI integration. Ud fra billeder og evt stikord, autoudfyld resten af felterne
- Overvej om AI kan rate billeder og give tips til forbedring?
- Overvej at implementer customerportal fra stripe, så brugere kan se deres abonnementer, men giver det værdi? https://dashboard.stripe.com/test/settings/billing/portal
- Når brugeren har lavet en specific søgning, da have popup der meget nemt tilbyder at oprette en boligagent ud fra netop den søgning
- Opsæt fornuftige hard limits på alt cloud som kan koste penge
- Måske få chatten til at brainstorme et farvetema med bootstrap, og inkluder det i dens settings så den husker det ved fremtidige kørseler
- Login redirect i middleware er broken
- Support JWT renewal
- Få styr på CORS, skal min app eksempelvis kun tillade fra enkelte domains?
- Sanitize ALT user input, evt lav form modeller til alt dette
- Ingen tal på tlf for create advertisement, selvom de eksisterer
- Opsæt automatiserede stripe simulations til tests i dev https://dashboard.stripe.com/test/billing/subscriptions/test-clocks
- Hvordan håndterer jeg anullerede subscriptions?
- Folk skal ikke kunne oprette flere subscriptions samtidig
- Overvej om betaling kan gøres endnu nemmere, ved at autoudfylde diverse felter for brugeren
- Hvad med skat? Stripe kan "collect tax automatically" https://stripe.com/docs/billing/taxes
- Google login integration
- Facebook login integration
- Lav cron job der automatisk disabler annoncer som er lagt op, men ikke længere er aktive. Måske er lejligheden nemlig solgt, eller det er spam
- Brug AI til at detektere/Valider/sanity check onde beskeder/billeder. Notificer mig da over mail og lad mig manuelt dobbelttjekke
Eller lad AI automatisk tildele folk strikes, man kan få 2-3 strikes og så auto ban
- Opnår vi optimal caching med requests til s3 billeder?
Optimer caching af billeder, se https://chatgpt.com/share/723cf2ef-93ca-40fc-ad79-c4176b0586f3
- Inkluder også sagsnummer på advertisement, det er mest for at give indtrykket af at vi har mange besøgende på siden
- Redirect til login page hvis bruger tilgår authenticated routes og IKKE er logged in
- Hav indbygget support for "Kun bytte" annoncer. Det skal integreres på en pæn måde, modsat hvordan DBA gør haha
- Optimer billede størrelse https://imagify.io/
- Hvis relevant, så kan adresser og en masse andet downloades her https://dawadownload.dataforsyningen.dk/adresser#danmark

# Lav frontend

- Optimering af markers på map. Måske kan vise små runde cirkler til at angive boliger, og først når vi er X zoomed ind bruge de pæne markers. Dette kræver dog at 
vi kan spørge google maps API'et hvilke koordinater der er i view således vi kun fremsøger de relevante fra backend. 
- Lav evt fane på home med de flotteste X boliger (rated af AI)
- Lav evt fane på home med de mest populære X boliger
- Lange adresser skal cutoff i home view, ellers forskyder de cards under
- Alle steder hvor vi har "alert()" skal vi i stedet vise en flot animation og beskrivelse
- Vis flot animation når annonce er oprettet
- Vis brugeren i GUI hvor længe der er tilbage af deres abonnement, for yderligere information link til deres stripe konto?
- Vil en flot transition på hover af cards give værdi? Evt hvor den viser nr 2 billede, hvis det eksisterer. Skal kun virke på desktop
- På detail view, evt lav knap "Kontakt sælger" som åbner en modal med kontaktinfo, tlf, mail og besked via siden
- Gør det nemt for brugeren at forstå og bruge AI i "Opret annonce" siden". Skriv ting som "Få hjælp til at udfylde felterne med AI" Eller "Lad AI tage sig af det hårde/kedelige arbejde"
- Hvis bruger tilgår detail view og bliver afvist pga manglende betaling, da send dem til en flot side hvor jeg sælger idéen om siden, hvor billigt det er og at det er 0 snyd. Skal være troværdigt. 
- Bliv inspireret af hvordan elbæk viser billeder i cards, de viser 1 af gangen på mobile. Skal vi vise 1 eller 2? https://elbaek.dk/alle-boliger/
- Udvid bootstrap classes med generisk styling til brug for hele frontend, eksempelvis hover effects på input felter
- Evt lav example multiselect i opret annonce view for rooms som her https://getbootstrap.com/docs/4.0/components/forms/#form-controls
- Refactor så alle input felter bruger ens components, eller lignende så vi altså kun har 1 type input felter
- Inspiration til home page/hook page se inspiration_homepage.png. Med tekst som: betal kun 30kr om ugen eller 100kr om måneden. Og nedenunder vis advertisement listings men i skjult format så folk ikke kan kontakte sælger.
  Hav FAQ i bunden. Få inspiration her https://mdbootstrap.com/docs/standard/extended/faq/#
- Såfremt brugeren har en annonce, da skift "Opret annonce" til "Se din annonce"
- Popup til boligagent når bruger laver søgning, se inspiration_boligagent.png
  Synes helt klart også der skal laves en virkelig flot homepage/hook hvor vi bruger billeder som nedenstående & titlen "Få adgang til dette og mange flere boliger". Billederne skal slef være taget af relle boliger når jeg har fået scrapet en masse.
  Tilsammen kunne denne homepage/hook bestå af overskrift øverst, så 3 facts på hvorfor de skal bruge siden (det er sindsygt billigt, 1000 vis af boliger (når jeg har scrapet), og så et billede af boliger cards og en FAQ til sidst
  inspiration_homepage_verynice_and_homemade.png](inspiration_homepage_verynice_and_homemade.png
- Find steder i home ui hvor jeg kan lokke brugeren til at trykke, men hvor det i stedet fører dem til login siden det kræver betaling eller login
- Enable modal eller lav anden løsning
- Når UI bygges skal alt JS/CSS minimizes & uglify til 1 fil
- Lav enten infinite scroll eller pagination på home page, vigtigt er dog at det er nemt at dele links til specifikke advertisements
- Det skal være så nemt som muligt for brugerne at oprette Andelsbolig annoncer
- Simplificer koden for pretty-button, kan ikke passe det skal fylde så meget lol
- Advertisement detail skal bruge dette endpoint @router.get("/advertisement/{_id}")
- Cards i advertisement_list kan simplificeres ved at udelade ord såsom "størrelse" & "månedlig ydelse", ersatat i stedet eksempelvis 3414 kr/måned og 100m2, det er nemlig selvforklarende
- Flot/letforståeligt billede eller animation på forsiden der viser meget kort hvordan det fungerer. Inkluder evt. ‘ekstremt billigt & fair’
- Tekst til siden "Billigste, bedste & nemmeste måde at sælge/købe din andelsbolig på"
- Vis views på boliger
- I søge bar evt tilføj knapper under søgebarne som brugeren kan vælge såsom ‘indenfor 30 km’ ‘øverst’
- Når man trykker på logo, transition/scroll brugeren ned lige under headeren
- Undersøg frontend mulighed som ham på LinkedIn nævnte
- Beskrivelse på abonnér siden. Målet skal være at gøre køberen tryg
‘Køb for kun 5kr om dagen, og få fuld adgang. Ingen skjulte gebyrer, ingen skjulte skeletter i skabet & straks opsigelse
- Lav animationer og transitions til alt, det er god UX
- Meget vigtigt. Find ud af hvordan jeg generelt skal håndtere forskellige screen sizes, således vi minimerer spildt arbejde. 
- Overvej at have 2 html filer, 1 til når man er logged ind og 1 til når man ikke er logget ind. Tror det kan simplificere koden.
- Popup når du trykker logud der skriver "Er du sikker på at du vil logge ud?" og så en "Ja" og "Nej" knap
- Gør det tydeligt at hvilke dele under "Opret bruger" som er kontaktinfo
- Hvis nødvendigt, bliv inspireret af Stripes frontend
- Understøt at brugere kan kontaktes på n antal emails & telefonnumre
- Når sider loader, vis en form for loading animation eller Lysegrå baggrund for der hvor elementer skal loades, giver betydeligt bedre UX. Se eksempel her https://buy.stripe.com/test_dR601Me4n9dr5ZSdQQ
- Ingen grund til at angive mail ved create view da det findes i brugerens jwt
- Vis 1/3 2/3 osv ved hvert billede nede i hjørnet
- Fremhæv brugerens egen profil på home med glowy Golden outline
- Oversæt brugervendt til dansk
- Der kan ryddes MEGET op i css filerne. Måske bruge bootstrap til at style det hele
- Overvej at have en "forside" som Dabea gør, hvor jeg sælger ideen om hjemmesiden og får folk hooked.
- Gør forsiden pæn. Skal virkelig have fokus på advertisement & advertisement_detail, især billede popup og resten
- Bliv generelt inspireret af Dabeas meget simple frontend design og look
- Når image uploades i create listing, da support at man kan trykke på et billede for at åbne den fulde version, evt som popup
- Tilbyd at lave beskrivelse om deres andelsbolig ved brug af AI
- Hvis de indtaster adresse skal så meget som muligt info automatisk fyldes ud
- Tegn/skitser UI layouts til side
- Overvej at lad brugeren vælge hvordan de vil kontaktes, når de opretter en advertisement
- Giv sælgere mulighed for at facilitere åbenthus via hjemme siden
- Kig på SEO, evt med lighthouse, og brainstorm med chatten
https://x.com/johnrushx/status/1844348205787697485?s=46&t=kVsKxdAIGgtnF5_B92O2YQ
Se SEO optimering keywords i inspirations_billeder/seo.png
For flere SEO tips se inspirations_billeder/seo_tips.png
- Under home/visning af advertisements skal brugeren kunne fremsøge sin egen ved at vælge en bool "Vis din annonce"
- Lazy load billeder så de først hentes når de er i skærmbilledet
- Hvordan skal vi vise mange advertisements? Liste? Infinite scroll?
Vær opmærksom på at state nok skal holdes i localstorage da vi ønsker at bibeholde bruger input selv når de skifter væk fra siden og kommer tilbage
- Lav sellers & buyers guide
- Vis 2 eller 4 billeder i listings, og et "+" hvis der er flere, som brugere kan klikke på for at se resten i fuld størrelse
- I detail view skal brugeren kunne åbne en popup der viser alle billeder (eller lignende)
- Ved lange sider, overvej at skifte baggrunden til en anden farve for bedre UX, ligesom Dabea gør her https://dabea.dk
- Price, monthly fee, login.password input felter størrelse skal matche andre input felter
- stripe buy button publishable-key skal ændres af env var
- Overvej at kunne vise flere annoncer på mobil som i inspiration_multiple inspiration_multiple_advertisements_homepage.png
- Intellij håndterer billeder på en god måde, hvis der er behov for inspiration til popup
- Overvej success screen hvor relevant se success.png
- Overvej om twitch cards kan noget, se twitch_cards.png
- Inkluder lidt skrift om hvorfor vi har behov for kontaktinfo på ‘opret bruger’ siden.
  Lav evt også designet lidt om til
  Horisontal linje
  Kontaktinfo
  Vi har brug for din kontaktinfo for at købere kan kontakte dig
- Når brugeren trykker på en advertisement og den brokker sig over login, da gør det så nemt som overhovedet muligt for brugeren at oprette en konto, helst med 1 klik direkte fra fejlbeskeden, ellers mister vi kunder lige dér.
  Eller vis modal popup til login
- Angiv for brugeren når ændringer i "Opret view" ikke er gemt
- Evt brug logoer fremfor form i detail view, ligesom boliga gør https://www.boliga.dk/bolig/2127032/pilestien_311_7190_billund
- Inspiration til hvordan vi kan vise billeder i cards. Man kan desuden trykke på billedet for at zoome  reddit_img.png

# Marketing strategi
- Først x måneder gratis for at få kunder til
- Skriv i FB grupper om hvordan det virker og at det er gratis
- Overvej at lave profiler til content på Instagram, Facebook, Twitter, LinkedIn for at markedsføre
- Ræk ud til andelsboligforeninger og nævn at hjemmesiden kan hjælpe med at sælge deres andelsboliger gratis og hurtigere
- Evt giv mulighed for at købe en "featured" annonce, som bliver vist øverst på siden
- Evt giv mulighed for at købe retten til at komme på forsiden
- Evt giv mulighed for at købe retten til at købere ikke behøver logge ind for at læse din annonce
- Evt giv mulighed for at købe ret til at få notifikation før alle andre, som køber
- Fortæl ChatGPT hvad mine target kunder er og lad den hjælpe med at målrette min markedsføring
- Måske inkluder dette i motto: "Få besked få sekunder efter en bolig kommer til salg, før alle andre"

# Security
- Rate limiting
- Beskyt mod XSS, somehow. 

# Features



# Infrastructure
- Mongo 7.0.0
- S3, i google cloud?


# Spørgsmål
- Hvilken s3 skal bruges
- Hvilken betalingsløsning skal bruges
- Hvad er marketingstrategien for at få kunder
- Hvad skal det koste
- Hvad skal domænet hedde




Favicon generator
https://favicon.io/favicon-converter/


## Stripe lokal testing
Event type docs https://docs.stripe.com/api/events/types
Stripe webhook GUI https://dashboard.stripe.com/test/webhooks

1. Kør stripe lokal med port forward
   PS C:\Users\Julian\Documents\stripe_1.21.2_windows_x86_64> .\stripe.exe listen --forward-to localhost:8500/webhook
2. Trigger webhook via deres console i GUI, eks:
stripe trigger checkout.session.complete


Material Design illustrations


# Learnings

## Bootstrap basics
Lær bootstrap basics, grid system, utility classes, CSS base components. https://getbootstrap.com/docs/5.1/getting-started/introduction/
  https://chatgpt.com/share/e35193c8-7535-48a1-9b6d-63e5407f9b5f


# Inden vi går live
- Køb reelt domæne
- Host hjemmesiden andet sted end github
- Opdater redirect linket i stripet https://dashboard.stripe.com/test/payment-links/plink_1Phs2KRwMNhLL1Z9Zcq2hDI2/edit

# Datafordeleren 
Hent addresser fra datafordeleren
https://confluence.sdfi.dk/pages/viewpage.action?pageId=10616849
Slå adresse op
https://api.dataforsyningen.dk/adgangsadresser/autocomplete?q=plantevej%20&type=adgangsadresse&side=1&per_side=100&noformat=1&srid=25832

Super smart address picker
https://danmarksadresser.dk/adresser-i-danmark/

Eksempel på bolig data
https://services.datafordeler.dk/DAR/DAR/3.0.0/rest/adresse?Format=JSON&id=0a3f50a3-f563-32b8-e044-0003ba298018


# Service account
andelsboligbasen@hidden-slice-416812.iam.gserviceaccount.com 

