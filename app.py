from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "edufocussecret"

# ================= LOGIN =================
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        nama = request.form.get("nama")
        if not nama:
            return render_template("login.html", error="Nama tidak boleh kosong")
        session.clear()
        session["user"] = nama
        session["total_belajar"] = 0
        session["total_soal"] = 0
        session["skor"] = 0
        session["deadlines"] = []
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ================= DASHBOARD =================
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

# ================= MOTIVASI =================
import random

motivasi_list = [
    "Tetap semangat, setiap langkah kecil itu berarti!",
    "Kesuksesan dimulai dari konsistensi hari ini.",
    "Jangan takut gagal, karena kegagalan adalah guru terbaik.",
    "Lakukan yang terbaik sekarang, dan hasilnya akan mengikuti.",
    "Setiap usaha akan membuahkan hasil jika sabar dan fokus."
]

@app.route("/motivasi")
def motivasi():
    if "user" not in session:
        return redirect("/")
    kata = random.choice(motivasi_list)
    return render_template("motivasi.html", kata=kata)


# ================= BELAJAR FOKUS =================
@app.route("/belajar")
def fokus():
    if "user" not in session:
        return redirect("/")
    return render_template("belajar.html")



# ================= UJIAN =================
soal_ujian = {
    "SD": {
        "Matematika":[
            {"soal":"5 + 7 = ?", "opsi":["10","11","12","13"], "jawaban":2},
            {"soal":"3 × 4 = ?", "opsi":["7","12","11","10"], "jawaban":1},
            {"soal":"9 - 3 = ?", "opsi":["5","6","7","4"], "jawaban":1},
            {"soal":"10 ÷ 2 = ?", "opsi":["4","5","6","7"], "jawaban":1},
            {"soal":"7 + 6 = ?", "opsi":["12","13","14","15"], "jawaban":1},
            {"soal":"8 - 5 = ?", "opsi":["2","3","4","5"], "jawaban":1},
            {"soal":"6 × 2 = ?", "opsi":["12","10","14","11"], "jawaban":0},
            {"soal":"15 ÷ 3 = ?", "opsi":["4","5","6","7"], "jawaban":1},
            {"soal":"9 + 4 = ?", "opsi":["12","13","14","15"], "jawaban":1},
            {"soal":"7 × 3 = ?", "opsi":["20","21","22","23"], "jawaban":1},
        ]
    },
    "SMP": {"Matematika":[
        {"soal":"12 × 3 = ?", "opsi":["36","35","34","33"], "jawaban":0},
        {"soal":"√49 = ?", "opsi":["6","7","8","9"], "jawaban":1},
        {"soal":"15 + 27 = ?", "opsi":["41","42","43","44"], "jawaban":3},
        {"soal":"50 ÷ 5 = ?", "opsi":["9","10","11","12"], "jawaban":1},
        {"soal":"5² = ?", "opsi":["10","20","25","30"], "jawaban":2},
        {"soal":"18 - 9 = ?", "opsi":["7","8","9","10"], "jawaban":2},
        {"soal":"6 × 6 = ?", "opsi":["35","36","37","38"], "jawaban":1},
        {"soal":"100 ÷ 4 = ?", "opsi":["24","25","26","27"], "jawaban":1},
        {"soal":"√64 = ?", "opsi":["6","7","8","9"], "jawaban":2},
        {"soal":"27 + 14 = ?", "opsi":["40","41","42","43"], "jawaban":1},
    ]},
    "SMA": {"Fisika":[
        {"soal":"Hukum Newton II = ?", "opsi":["F=ma","F=m/g","F=v×m","F=m+v"], "jawaban":0},
        {"soal":"Kecepatan = ?", "opsi":["v=s/t","v=t/s","v=s×t","v=t×s"], "jawaban":0},
        {"soal":"Percepatan = ?", "opsi":["a=v/t","a=t/v","a=v×t","a=t×v"], "jawaban":0},
        {"soal":"Gaya = ?", "opsi":["F=ma","F=m/v","F=v×a","F=m+a"], "jawaban":0},
        {"soal":"Energi kinetik = ?", "opsi":["1/2mv²","mv²","1/2m²v","m²v²"], "jawaban":0},
        {"soal":"Momentum = ?", "opsi":["p=mv","p=m/v","p=v/m","p=m+v"], "jawaban":0},
        {"soal":"Hukum Hooke = ?", "opsi":["F=kx","F=k/x","F=x/k","F=k+x"], "jawaban":0},
        {"soal":"Tekanan = ?", "opsi":["P=F/A","P=F×A","P=A/F","P=F+A"], "jawaban":0},
        {"soal":"Frekuensi = ?", "opsi":["f=1/T","f=T","f=T²","f=T/2"], "jawaban":0},
        {"soal":"Gelombang = ?", "opsi":["v=fλ","v=f/λ","v=f+λ","v=λ/f"], "jawaban":0},
    ]}
}


@app.route("/utbk", methods=["GET", "POST"])
def utbk():
    if "user" not in session:
        return redirect("/")

    # Data soal per subtest (minimal 10 soal tiap subtest)
    soal_list = {
        "Penalaran Umum": [
            {"soal": "Berapakah hasil 2 + 3?", "opsi": ["4","5","6","7"], "jawaban":1},
            {"soal": "Jika semua kucing bernapas, maka semua kucing adalah...", "opsi":["hewan","tumbuhan","ikan","burung"], "jawaban":0},
            {"soal": "Lengkapi pola: 2, 4, 8, 16, ?", "opsi":["32","24","20","18"], "jawaban":0},
            {"soal": "Bentuk kebalikan dari kata 'baik' adalah...", "opsi":["jahat","buruk","lemah","besar"], "jawaban":1},
            {"soal": "Jika A>B dan B>C, maka hubungan antara A dan C?", "opsi":["A<C","A=C","A>C","Tidak bisa ditentukan"], "jawaban":2},
            {"soal": "Pilih kata yang tidak sepadan: apel, jeruk, pisang, mobil", "opsi":["apel","jeruk","pisang","mobil"], "jawaban":3},
            {"soal": "Jika semua burung bisa terbang, maka burung unta bisa?", "opsi":["Terbang","Tidak","Kadang","Tidak bisa ditentukan"], "jawaban":3},
            {"soal": "Pilih angka yang tepat: 5, 10, 20, 40, ?", "opsi":["80","70","90","100"], "jawaban":0},
            {"soal": "Jika semua X adalah Y dan semua Y adalah Z, maka semua X adalah?", "opsi":["Y","Z","Tidak bisa ditentukan","X"], "jawaban":1},
            {"soal": "Sinonim kata 'besar' adalah...", "opsi":["kecil","tinggi","luas","hebat"], "jawaban":3}
        ],
        "Matematika": [
            {"soal": "Berapakah 7×6?", "opsi":["42","36","48","40"], "jawaban":0},
            {"soal": "Jika x=3, 2x+5=?", "opsi":["8","9","10","11"], "jawaban":3},
            {"soal": "Berapakah 12 : 4?", "opsi":["2","3","4","6"], "jawaban":1},
            {"soal": "Jika 5x=25, x=?","opsi":["4","5","6","7"], "jawaban":1},
            {"soal": "Hasil dari 15+27?", "opsi":["42","40","43","44"], "jawaban":0},
            {"soal": "Berapakah akar kuadrat dari 81?", "opsi":["8","9","10","11"], "jawaban":1},
            {"soal": "Jika y-3=7, y=?","opsi":["9","10","11","12"], "jawaban":2},
            {"soal": "Berapakah 9×9?", "opsi":["81","72","91","80"], "jawaban":0},
            {"soal": "Pilih hasil yang benar: 50-15=?","opsi":["30","35","40","45"], "jawaban":1},
            {"soal": "Jika x+7=12, x=?","opsi":["4","5","6","7"], "jawaban":1}
        ],
        "Bahasa Indonesia":[
            {"soal":"Sinonim kata 'cepat' adalah...", "opsi":["lambat","kilat","pelan","malas"], "jawaban":1},
            {"soal":"Antonim kata 'panjang' adalah...", "opsi":["pendek","lebar","tinggi","besar"], "jawaban":0},
            {"soal":"Kata yang baku: 'telepon' atau 'telpon'?", "opsi":["telepon","telpon","telphon","teplefon"], "jawaban":0},
            {"soal":"Kata 'murid' sepadan dengan...", "opsi":["guru","siswa","teman","anak"], "jawaban":1},
            {"soal":"Sinonim kata 'senang' adalah...", "opsi":["sedih","bahagia","murung","marah"], "jawaban":1},
            {"soal":"Pilih kata yang salah ejaan: buku, meja, lampar, pensil", "opsi":["buku","meja","lampar","pensil"], "jawaban":2},
            {"soal":"Antonim kata 'tinggi' adalah...", "opsi":["pendek","rendah","kecil","lebar"], "jawaban":1},
            {"soal":"Sinonim kata 'besar' adalah...", "opsi":["kecil","luas","tinggi","sedikit"], "jawaban":1},
            {"soal":"Kata baku dari 'kantor pos' adalah...", "opsi":["kantor pos","kantorpos","kantor-pos","kantorPos"], "jawaban":0},
            {"soal":"Pilih kata yang tidak sepadan: kucing, anjing, mobil, kelinci", "opsi":["kucing","anjing","mobil","kelinci"], "jawaban":2}
        ]
    }

    # POST submit skor
    if request.method == "POST":
        subtest = request.form.get("subtest")
        skor = 0
        total = len(soal_list[subtest])
        for i, s in enumerate(soal_list[subtest]):
            val = request.form.get(f"q{i}")
            if val is not None and int(val) == s["jawaban"]:
                skor += 1
        # update session untuk progres
        session["total_soal"] = session.get("total_soal", 0) + total
        session["skor"] = session.get("skor", 0) + skor
        return render_template("utbk.html", soal=soal_list, submit=True, skor=skor, subtest=subtest)

    return render_template("utbk.html", soal=soal_list)


# ================= PROGRESS =================
@app.route("/progress")
def progress():
    if "user" not in session:
        return redirect("/")
    data = {
        "total_belajar": session.get("total_belajar",0),
        "total_soal": session.get("total_soal",0),
        "skor": session.get("skor",0)
    }
    return render_template("progress.html", data=data)


# ================= DEADLINE =================
@app.route("/deadline", methods=["GET","POST"])
def deadline():
    if "user" not in session:
        return redirect("/")
    if request.method == "POST":
        tugas = request.form.get("tugas")
        tanggal = request.form.get("tanggal")
        session["deadlines"].append({"tugas":tugas,"tanggal":tanggal})
        session.modified = True
    return render_template("deadline.html", deadlines=session["deadlines"])


# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
