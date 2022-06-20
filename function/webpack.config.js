// Generated using webpack-cli https://github.com/webpack/webpack-cli
const NodePolyfillPlugin = require("node-polyfill-webpack-plugin")
const path = require('path');

const config = {
    entry: './src/index.js',
    output: {
        path: path.resolve(__dirname, 'dist'),
    },
    plugins: [
        new NodePolyfillPlugin()
    ],
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/i,
                loader: 'babel-loader',
            },

            // Add your rules for custom modules here
            // Learn more about loaders from https://webpack.js.org/loaders/
        ],

    },
    devtool: 'cheap-module-source-map',
    resolve: {
        alias: {
            "fs": false,
            util: require.resolve("util/")
        }
    }
};

module.exports = () => {
    config.mode = 'development';
    return config;
};
