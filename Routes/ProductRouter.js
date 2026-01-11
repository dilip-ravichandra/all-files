const express = require('express');
const ensureAuthenticated = require('../Middlewares/Auth');

const router = express.Router();

router.get('/', ensureAuthenticated, (req, res) => {
    console.log('---loged in user details---',req.user);
    res.status(200).json({
        message: 'Protected products fetched successfully',
        user: req.user, // comes from JWT
        products: [
            {
                name: "Mobile",
                price: 10000
            },
            {
                name: "TV",
                price: 20000
            }
        ]
    });
});

module.exports = router;
