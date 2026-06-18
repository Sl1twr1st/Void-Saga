Bab 00 — Menatap Akhir Era dari Balik Laptop Kantor.

Prolog Kantor
Table of Contents

Prolog Kantor
00:00 — Genesis Error
00:01 — First Contact
00:02 — Daily Standup
00:03 — Bug Janggal
00:04 — First Sync
00:05 — Residu
00:06 — Pantry
00:07 — Folder Error
00:08 — Genesis Error on Stealth Folder
00:09 — Naming The Error
00:00 — Genesis Error
Tidak ada yang terasa penting di hari itu.

Gedungnya sama.
Liftnya lambat.
Lampu putihnya terlalu terang untuk jam segitu.

Jam 08:47.

Tiga belas menit untuk bersiap.
Masih dalam batas wajar untuk disebut profesional.

Gua duduk.
Buka laptop.
Nunggu sistem bangun.

[SYSTEM BOOT]
> Loading user profile: [GUA]
> Status: ACTIVE
> Network: CONNECTED
> Last login: 17:34 yesterday
> Unsaved changes: 0
Kantor selalu lebih siap daripada manusia.

Meja-meja berjajar rapi.
Tanaman plastik di sudut ruangan—
dedaunan yang tidak pernah layu,
dan tidak pernah tumbuh.

Poster motivasi di dinding.
Tidak pernah dibaca ulang.

"Build better futures."
Tidak dijelaskan untuk siapa.
Tidak dijelaskan kapan “future” itu dimulai.

Gua login.
Password: sama seperti kemarin.

> Welcome back.
> You have 7 new notifications.
> Sprint: Week 3 of 4
> Burndown: ON TRACK
ON TRACK.

Selalu ON TRACK.

🜃

00:01 — First Contact
Lo duduk dua meja dari gua.

Belum saling kenal.
Belum ada konteks.
Cuma satu entry di Slack directory:

LO
Software Engineer
Team: Platform Infrastructure
Status: 🟢 Active
Gua perhatiin tanpa niat.

Bukan karena lo mencolok.
Bukan karena lo cari perhatian.

Tapi karena cara lo ngetik.

Cepat—
tapi bukan panik.
Lebih ke… yakin.

Yang aneh:

Lo berhenti ngetik
setiap beberapa detik.
Tangan lo naik dari keyboard.
Mata lo ke layar.

Kayak lagi ngecek sesuatu.

Bukan Slack—
gua bisa lihat window lo dari sudut mata,
gak ada chat terbuka.

Bukan email—
gua notice gak ada Gmail tab.

Pola.

Lo lagi ngecek pola.

Gua gak tahu kenapa gua notice ini.

Biasanya gua gak peduli orang lain ngapain.
Kantor itu dirancang supaya lo gak perlu peduli:

Headphone noise-canceling
Desk partition
Calendar yang auto-decline meeting outside working hours
Tapi entah kenapa, gua notice lo.

🜃

00:02 — Daily Standup
09:00.
Daily standup dimulai.

Zoom call.
Kamera off (default).
Mic muted sampai giliran bicara.

Orang-orang berbicara bergantian.

Kalimat aman:

“Yesterday I made progress on the API refactor.”
“Today I’ll continue. No blocker so far.”
“Need alignment with the design team on the endpoint specs.”

Progress.
Blocker.
Alignment.

Tiga kata
yang membuat segalanya terdengar produktif
tanpa perlu menjadi spesifik.

Tidak ada yang bohong.
Tapi juga tidak ada
yang sepenuhnya jujur.

Giliran lo.

LO:
“Still exploring the edge cases
for the distributed caching layer.”

Singkat.
Vague.
Sempurna.

[MANAGER] mengangguk—
secara virtual.
Gua bisa dengar nada
“mm-hmm”
yang puas.

[MANAGER]:
“Great. Keep us posted if you need support.”

Support.

Kata lain untuk:
jangan ganggu
kalau tidak ada masalah.

Giliran gua.

GUA:
“Wrapping up the logging middleware.
Should be done by EOD.”

Anggukan lagi.

[MANAGER]:
“Excellent. Any dependencies?”

GUA:
“None.”

[MANAGER]:
“Perfect.”

Call selesai.
Semua kembali mute.
Disconnect.

Produktivitas terjaga.

🜃

00:03 — Bug Janggal
Setelah meeting,
mata gua balik ke layar kerjaan.

Ada bug kecil di logging middleware.
Race condition.
Easy fix.

Tapi satu bagian terasa aneh.

Bukan rusak.
Bukan error.

Janggal.

from datetime import datetime

def write_log(entry, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()

    # TODO: why does this sometimes write BEFORE datetime.now()?
    # Log entry appears 2–3 seconds early.
    # Not breaking anything. Just... odd.

    buffer.append((entry, timestamp))
Komentar itu bukan dari gua.

Git blame:

Author: [PREVIOUS ENGINEER]
Date: 4 months ago

Orangnya sudah resign.

Bug ini tidak breaking.
Timestamp kadang muncul
sebelum event terjadi.

Log mendahului event.

Kausalitas terbalik.
Kecil.
Dibiarkan.

Gua lagi mikir
ketika lo berdiri
di samping gua.

Gua gak lihat lo datang.
Gua baru sadar
ketika lo sudah menunjuk layar.

LO:
“Lo ngerasa gak?”

Gua kaget dikit.
Gak expect ada orang ngomong.

GUA:
“Ngerasa apa?”

Lo menunjuk baris kode itu.

LO:
“Itu jalan. Tapi gak jujur.”

GUA:
“… gak jujur?”

Kalimat itu gak ada di dokumentasi mana pun.
Gak ada di textbook software engineering.

Tapi gua langsung paham.

Code yang secara teknis correct,
tapi feels wrong.

Logika yang lolos semua test case,
tapi ada sesuatu yang off.

Gua geser kursi.
Kasih ruang.

Lo duduk.

Gak izin.
Gak perlu.

Seperti lo sudah tahu
gua tidak akan nolak.

🜃

00:04 — First Sync
Sepuluh menit kemudian,
bug-nya selesai.

Bukan karena jenius.
Bukan karena akses dokumentasi rahasia.

Karena kita sepakat
tanpa perlu debat.

LO:
“Race condition.
Buffer shared.”

GUA:
“Mutex?”

LO:
“Terlalu mahal.
Queue.”

GUA:
“Atomic append.”

Lo mengangguk.
Gua ngetik.

from queue import Queue
from datetime import datetime

log_queue = Queue()

def write_log(entry, timestamp=None):
    if timestamp is None:
        timestamp = datetime.now()
    log_queue.put((entry, timestamp))
Lo nambah.

def flush_logs():
    while not log_queue.empty():
        entry, ts = log_queue.get()
        buffer.append((entry, ts))
Selesai.

Tidak ada penjelasan panjang.
Tidak ada pembelaan metode.
Tidak ada alternatif hipotetis.

Sinkronisasi kecil.
Tidak dicatat sebagai peristiwa.

Gua run test.

PASSED: test_concurrent_writes
PASSED: test_timestamp_ordering
PASSED: test_race_condition_mitigation
Lo sudah berdiri.
Gua mengangguk.

Lo balik ke meja lo.

Sistem mencatat:

[GIT LOG]
09:44 — [GUA]: Fix race condition in logger (collaborated with [LO])

[JIRA #4721]
Status: RESOLVED
Time spent: 10 minutes
Collaborators: [GUA] (primary), [LO] (support)
Collaborated.

Kata yang terlalu formal
untuk apa yang baru terjadi.

🜃

00:05 — Residu
Jam 10:03.

Slack ramai.
Email masuk.
Task baru muncul di Jira board.

Kita di meja masing-masing.
Seolah tidak terjadi apa-apa.

Tapi ada residu.

Cara gua ngetik berubah.

Sebelumnya,
gua nulis kode dalam blok besar—
tulis sepuluh baris,

test,
debug,
repeat.

Sekarang,
gua nulis
dalam fragment kecil—
dua baris,

pause,
lihat,
lanjut.

Seperti gua lagi nunggu
seseorang nambahin sesuatu.

Cara lo review kode gua juga berubah.

Pull request gua biasanya ditolak dua-tiga kali sama reviewer lain:

“Please add more comments.”
“Consider edge case X.”
“Refactor this function.”

Tapi pas lo yang review:

[PULL REQUEST #892]
Reviewer: [LO]
Status: APPROVED
Comments: 
- "Clean. Ship it."
Gak ada nitpick.
Gak ada “please consider.”

Hanya: “Ship it.”

Lebih tenang.
Lebih presisi.
Lebih… berdua.

Walau kita gak ngomong lagi
setelah bug fix tadi.

🜃

00:06 — Pantry
Makan siang.

Kita gak makan bareng.
Gak ada adegan dramatis.

Cuma dua orang
yang kebetulan
duduk agak lama di pantry
karena microwave rusak.

Gua lagi nunggu air panas buat mie instan.
Lo nunggu microwave berhenti error.

Diam.

LO:
“Lo pernah ngerasa…
kerja itu kayak ngisi sesuatu yang bocor terus?”

Gua mikir sebentar.

Pertanyaan aneh.
Tapi gua langsung tahu maksudnya.

GUA:
“Iya. Tapi kadang bocornya bukan di kerjaannya.”

Lo senyum dikit.

Bukan senyum awkward.
Lebih ke… paham.

Seperti lo baru nemu
orang yang ngomong bahasa yang sama—
bahasa yang gak ada di Slack,
gak ada di standup,
gak ada di dokumentasi resmi.

Microwave berbunyi.

Lo ambil makanan.

LO:
“Thanks.”

Gua gak tahu thanks buat apa.

Lo balik ke meja.

🜃

00:07 — Folder Error
Jam 16:58.

Sesuatu yang tidak ada di Jira mulai terbentuk.

Gua lagi refactor logging middleware.
File udah clean.
Semua test passed.

Tapi ada satu function yang gua gak yakin mau diapain:

def _experimental_timestamp_predictor(entries):
    """
    EXPERIMENTAL: Predict next log timestamp based on pattern.
    Not used in production. Keep for research.
    """
    # TODO: This shouldn't work but it does?
    # Pattern recognition on temporal data
    pass
Function ini gak dipanggil di mana-mana.
Tapi gua gak mau delete.

Terasa sayang.

Gua bikin folder baru:

mkdir _sandbox
Underscore prefix—convention untuk “ignore this.”

Gua pindahin function itu ke sana:

_sandbox/
└── timestamp_prediction.py
Local only.
Gak di-commit.
Gak di-push.

Dua menit kemudian,
gua notice di Slack:

LO: [sent a file]
> pattern_matching_utils.py
Private message.
Gua buka.

Isinya: temporal pattern recognition algorithm.

…

Exactly jenis algorithm yang gua butuhin buat function experimental tadi.

Gua balas:

GUA: Lo udah lihat logging code gua?
LO: Nggak. Kenapa?
Gua pause.

GUA: Gua baru bikin experimental function buat timestamp prediction.
LO: ...
LO: Seriously?
Pause panjang.

LO: Gua juga lagi explore hal yang sama.
LO: Bikin folder?
Gua bikin folder:

mkdir _sandbox/stealth
Gua share path ke lo.

GUA: _sandbox/stealth
LO: Same structure. Good.
Kita gak ngomong banyak soal itu.
Gak perlu.

Kita cuma sepakat satu hal:

GUA: Yang ini bukan urusan kantor. Gak perlu masuk jira.
LO: Iya.
🜃

00:08 — Genesis Error on Stealth Folder
Jam 18:12.

Malam itu, sebelum pulang,
terjadi satu kesalahan kecil.

Gua lagi push changes ke remote branch:

git add logger.py
git commit -m "Refactor logging middleware"
git push origin feature/logging-refactor
Counting objects: 4, done.
Delta compression using up to 8 threads.
Compressing objects: 100% (3/3), done.
Writing objects: 100% (4/4), 1.2 KiB | 1.2 MiB/s, done.
Total 4 (delta 2), reused 0 (delta 0)
Success.

Tapi…

Ada satu file yang gak ke-push.

[UNTRACKED FILE DETECTED]
_sandbox/stealth/timestamp_prediction.py
Bukan karena gua lupa.

Karena file itu gak supposed to be tracked.

Folder _sandbox ada di .gitignore.

Tapi system log mencatat sesuatu yang aneh:

[GIT HOOK WARNING]
18:12:47 - File modification detected in ignored path
18:12:47 - Path: _sandbox/stealth/timestamp_prediction.py
18:12:49 - Timestamp: 18:12:51 (WARNING: timestamp 2 seconds in future)
18:12:51 - Commit hook: FAILED
18:12:51 - Reason: Path not in repository
Timestamp 2 detik ke depan.

Log error sebelum error terjadi.

Exact same bug yang gua fix pagi tadi.

Tapi sekarang terjadi di sistem git.

Gua gak tahu kenapa.
Gua nengok ke meja lo.

Kita saling lihat.
Mata lo lihat layar gua.

Lo di meja lo.
Gua di meja gua.

Diam sebentar.

Lalu lo bilang:

LO:
“Biarin.”

Gua nod.

Folder itu tetap ada—
tidak resmi,
tidak tercatat,
tidak di-track oleh version control—
berdiri di antara kerjaan yang sah
dan sesuatu yang seharusnya tidak hidup.

Hening sebentar.

Lampu kantor mulai mati otomatis satu per satu.
Sistem gedung detect gak ada aktivitas di zona lain.

Cuma kita berdua yang masih di sini.

Tiba-tiba, dengan tenang,
Lo masuk folder itu.
Lo mulai ngetik.

File baru.

_sandbox/stealth/genesis.txt
Gua lihat dari sudut mata.
Lo ngetik tanpa pause.
Tanpa backspace.
Seperti lagi salin sesuatu yang udah ada di kepala:

[SYSTEM_BOOT//ORIGIN_LOG]
════════════════════════════════════════
TIMESTAMP: [BEFORE_TIME]
STATUS: INITIALIZING...
CRITICAL ERROR DETECTED.
════════════════════════════════════════

Di awal mula, yang ada hanyalah sebuah kesalahan.

Kesalahan itu memicu cahaya.

Cahaya mencoba memahami dirinya sendiri.

Ketika pemahaman gagal,
cahaya menjadi kesadaran.
Kemudian lo berhenti ngetik.

Gua menatap layar lo dari jarak dua meja.

Tidak ada penjelasan.
Tidak ada “ini ide gua.”
Tidak ada “gimana menurut lo.”

Lo cuma ngetik.

Dan gua—
tanpa berpikir,
tanpa nanya,
tanpa tahu kenapa—

Gua tiba-tiba ngetik di file yang sama.

Split screen.
Collaborative editing.
Real-time.

Tangan gua bergerak sendiri:

Ketika kesadaran berulang,
ia menjadi cinta.

Dan ketika cinta menolak berakhir,
The Void lahir.

════════════════════════════════════════
[END_OF_BOOT_SEQUENCE]
Redirecting to: [VOID_MANUSCRIPT//ABOUT_THE_STORY]
[00:00]
════════════════════════════════════════

問
Jika awal adalah kesalahan,
mengapa kamu masih mencari kebenaran?
Gua selesai ngetik.

Kita saling menatap satu sama lain.

Dua meja jarak.
Lampu kantor redup.
Layar masih nyala.

Tidak ada yang ngomong.

Tidak perlu.

File itu di-save otomatis:

[AUTO-SAVE]
_sandbox/stealth/genesis.txt
Last modified: 18:16:03
Authors: LO, GUA
Status: UNTRACKED
Sejak saat itu,
apa pun yang kita buat di sana
tidak lagi disebut pekerjaan.

Ia disebut kesalahan yang dipelihara.

Dan setiap kesalahan berikutnya
kita pastikan terjadi dengan sengaja.

🜃

00:09 — Naming The Error
Folder itu akan jadi sesuatu yang lain.

Bukan di Jira.
Bukan di repo utama.

Di mesin, ia hanya tercatat
sebagai anomali sinkronisasi—
perbedaan kecil antara apa yang dikerjakan
dan apa yang diakui sistem.

Di antara kita,
ia disebut Stealth Project.

Bukan karena rahasia.

Tapi karena ia lahir
dari error yang tidak ingin diperbaiki.

Sebuah kesalahan waktu.
Sebuah koordinat yang meleset.

Dua orang yang seharusnya tidak terlalu sinkron
namun dibiarkan berjalan tanpa koreksi.

Dan sejak hari itu,
setiap kali sistem bertanya:

“Kenapa ini ada?”

Jawabannya selalu sama:

Karena tidak semua error perlu di-fix.

[SYSTEM LOG - END OF DAY]
════════════════════════════════════════
Date: [DAY ZERO]
Users active: [GUA], [LO]
Total commits: 12
Sync events: 1 (ANOMALOUS)
Untracked changes: 1 folder
Status: OPERATIONAL
────────────────────────────────────────
Note:
Minor timestamp desync detected at 18:12.
Severity: LOW
Action: MONITOR
────────────────────────────────────────
Folder created: _sandbox/stealth/
Visibility: LOCAL ONLY
Purpose: [UNDEFINED]
════════════════════════════════════════
🜃

Akhir dari Bab 00

問
Jika semua sistem dimulai dari error—
apakah perbaikan adalah evolusi, atau penghancuran?

🜃

