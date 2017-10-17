# LibreOffice LangPack

Sada LangPack receptů má za úkol dostat do Munki repozitáře instalační balíček s aktuální jazykovým balíčkem Pro LibreOffice. Toto je potřeba, pokud chceme  LibreOffice mít možnost přepnout do češtiny a provádět kontrolu pravopisu.

Recepty provedou několik kroků:

1. stáhnutí aktuální verze LibreOffice;
2. stáhnutí aktuální verze vybraného jazykového balíčku;
3. zjištění skutečné verze LibreOffice (verze jazykové balíčku někdy mají uvedenou verzi jinak);
4. extrakce souborů z jazykové balíčku a vytvoření instalačního .pkg balíčku;
5. import instalačního balíčku do Munki repozitáře; 
6. úprava klíče **version** v pkginfo souboru uvnitř Munki repozitáře;

Naše řešení je funkční, má však řadu nedostatků, které nevíme, jak v rámci AutoPkg řešit (pokud to vůbec lze). Problémy jsme popsali v diskuzní google AutoPkg [skupině](https://groups.google.com/forum/#!topic/autopkg-discuss/2MuGE1UHUhs). Ve zkratce:

- Pro zjištění korektní verze LibreOffice je třeba stáhnout kompletní LibreOffice balík, což většinou znamená, že se LibreOffice balík stahuje 2x.
- Bylo nutné napsat krátký Python modul na zálohování proměnné, která by jinak byla přepsána.
- Spouštění receptu skončí chybou, pokud není dostupná nová verze jazykového balíčku. Toto je důsledek posledního kroku, který modifikuje pkgsinfo soubor v Munki, kam zapisuje korektní verzi balíčku.

