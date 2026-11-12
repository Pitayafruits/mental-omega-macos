#!/usr/bin/env python3
"""Build an original-rules wrapper from user-supplied game files and Wine."""
import argparse,configparser,plistlib,shutil,subprocess
from pathlib import Path
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--game-dir',required=True,type=Path)
p.add_argument('--engine-app',required=True,type=Path)
p.add_argument('--output',type=Path,default=Path('dist/Mental Omega.app'))
a=p.parse_args();game=a.game_dir.resolve();engine=a.engine_app.resolve();out=a.output.resolve();repo=Path(__file__).resolve().parents[1]
for name in ['gamemd.exe','ra2.mix','ra2md.mix','language.mix','langmd.mix','BINKW32.dll','BLOWFISH.dll','Syringe.exe']:
 if not (game/name).is_file():p.error('Missing game file: '+name)
if not (engine/'Contents/Resources/wine/bin/wine').is_file():p.error('Unsupported Wine app layout')
if out.exists():p.error('Output already exists; choose a new output path')
r=out/'Contents/Resources';r.mkdir(parents=True);(out/'Contents/MacOS').mkdir()
for source,target in [(game,r/'Game'),(engine,r/'Engine.app')]:subprocess.run(['ditto',str(source),str(target)],check=True)
g=r/'Game'
for name in ['SoloData','SoloLauncher.exe','Client','debug','Saved Games','Screenshots','spawn.ini','spawnmap.ini','stats.dmp','syringe.log']:
 q=g/name
 if q.is_dir():shutil.rmtree(q)
 elif q.exists():q.unlink()
for name in ['Client','debug','Saved Games','Screenshots']:(g/name).mkdir()
for file in ['ClientDefinitions.ini','GameOptions.ini']:
 q=g/'Resources'/file;c=configparser.ConfigParser(strict=False,interpolation=None);c.optionxform=str;c.read(q,encoding='utf-8-sig')
 if file=='ClientDefinitions.ini':c.set('Settings','GameLauncherExecutableName','Syringe.exe')
 else:c.set('cmbCredits','Items','50000,40000,30000,20000,10000,7500,5000');c.set('cmbCredits','DefaultIndex','4')
 with q.open('w',encoding='utf-8-sig') as f:c.write(f,space_around_delimiters=False)
q=g/'RA2MO.ini';c=configparser.ConfigParser(strict=False,interpolation=None);c.optionxform=str;c.read(q,encoding='utf-8-sig');c.set('MultiPlayer','Handle','Player')
with q.open('w') as f:c.write(f,space_around_delimiters=False)
shutil.copy2(repo/'src/launch-game.sh',r/'launch-game.sh')
subprocess.run(['clang','-mmacosx-version-min=11.0','-fobjc-arc','-framework','Cocoa','-arch','arm64','-arch','x86_64',str(repo/'src/Launcher.m'),'-o',str(out/'Contents/MacOS/MentalOmega')],check=True)
info={'CFBundleName':'Mental Omega','CFBundleIdentifier':'local.mentalomega.mac.original','CFBundleExecutable':'MentalOmega','CFBundlePackageType':'APPL','CFBundleShortVersionString':'3.3.6','CFBundleVersion':'1','LSMinimumSystemVersion':'11.0','NSPrincipalClass':'NSApplication','NSHighResolutionCapable':True}
(out/'Contents/Info.plist').write_bytes(plistlib.dumps(info))
subprocess.run(['codesign','--force','--sign','-',str(out)],check=True)
print(out)
