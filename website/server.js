import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import nunjucks from "nunjucks";
import { spawn } from "child_process";
import session from "express-session";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));
app.use(express.json());
app.use(session({
    secret: "secret",
    resave: false,
    saveUninitialized: true
}))

nunjucks.configure(path.join(__dirname, "views"), {
    autoescape: true,
    express: app,
    watch: true,
});

// app routes
app.get("/", (req, res) => {
    res.render("index.html", { title: "Home" });
});

app.get("/login", (req, res) => {
    res.render("login.html")
})

app.get("/register", (req, res) => {
    res.render("register.html")
})

app.get("/user", (req, res) => {
    res.render("user.html", { username: "username", email: "email", phoneNumber: "phoneNumber" })
})

app.get("/admin", (req, res) => {
    res.render("admin.html")
})

// app post
app.post("/auth", (req, res) => {
    const { username, password } = req.body;
})

app.post("/reg", (req, res) => {
    const { username, email, password, phoneNum } = req.body
})

// python shell test
app.post("/generateExcuse", (req, res) => {
    const scriptPath = path.join(__dirname, "../ml", "inference.py");
    const python = spawn("python", [scriptPath]);

    const { situation, context, seriousness, length } = req.body;
    const data = JSON.stringify({ situation, context, seriousness, length });

    python.stdin.write(data);
    python.stdin.end();

    let output = "", errorMsg = ""
    python.stdout.on("data", data => output += data.toString());
    python.stderr.on("data", err => errorMsg += err.toString());

    python.on("close", code => {
        if (code !== 0) {
            console.error(errorMsg);
            return res.status(500).send(errorMsg);
        }

        try {
            const jsonData = JSON.parse(output);
            res.json(jsonData);
        } catch (err) {
            console.error("JSON parse error: ", err);
            res.status(500).send("JSON parse error");
        }
    });
});

// listener
app.listen(3000, () => {
    console.log("Server started at http://localhost:3000")
})

