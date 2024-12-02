if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config()
}

const express = require('express')
const app = express()
const path = require('path')
const bcrypt = require('bcrypt')
const passport = require('passport')
const flash = require('express-flash')
const session = require('express-session')

const initializePassport = require('./passport-config')
initializePassport(
    passport, 
    username => users.find(user => user.username === username)
)

app.use(express.static(path.join(__dirname, 'public')));
app.set('view-engine', 'ejs')
app.use(flash())
app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false
}))
app.use(passport.initialize())
app.use(passport.session())

app.use(express.urlencoded({extended: false}))

const users = []

app.get('/', (req, res) => {
    res.render('tabs.ejs')
})

app.get('/login', (req, res) => {
    res.render('login.ejs'), { message: req.flash('error') }
})

app.post('/login', passport.authenticate('local', {
    successRedirect: '/',
    failureRedirect: '/login',
    failureFlash: true
}))

app.get('/register', (req, res) => {
    res.render('register.ejs')
})

app.post('/register', async (req, res) => {
    try {
        const hashedPassword = await bcrypt.hash(req.body.password, 10)
        users.push({
            id: Date.now().toString(),
            name: req.body.username,
            password: hashedPassword
        })
        res.redirect('/login')
    } catch {
        res.redirect('/register')
    }

})

app.get('/tab0', (req, res) => {
    res.render('tab_0.ejs')
})

app.get('/tab1', (req, res) => {
    res.render('tab_1.ejs')
})

app.get('/tab2', (req, res) => {
    res.render('tab_2.ejs')
})

app.get('/tab3', (req, res) => {
    res.render('tab_3.ejs')
})

app.listen(3000)