const LocalStrategy = require('passport-local').Strategy
const bcrypt = require('bcrypt')

function initialize(passport, getUserByUsername, getUserByID) {
    const authenticateUser = async (username, password, done) => {
        const user = getUserByUsername(username)
        if (user == null){
            return done(null, false, { message: 'No user with that username' })
        }

        try {
            if (await bcrypt.compare(password, user.password)) {
                return done(null, user)
            } else {
                return done(null, false, { message : 'Password incorrect '})
            }
        } catch (e) { 
            return done(e)
        }
    }

    passport.use(new LocalStrategy({ usernameField: 'username' }, authenticateUser))
    passport.serializeUser((user, done) => done(null, user.id))
    passport.deserializeUser((id, done) => { 
        const user = getUserByID(id)
        if(user) {
            done(null, user)
        } else {
            done(new Error('User not found'), null)
        }
        // return done(null, getUserByID(id))
    })
}

module.exports = initialize