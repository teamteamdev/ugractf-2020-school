const path = require('path');
const webpack = require('webpack')

module.exports = {
    entry: './src/server.ts',
    mode: 'production',
    module: {
        rules: [
            {
                test: /\.ts$/,
                use: 'ts-loader'
            }
        ]
    },
    output: {
        filename: 'server.js',
        path: path.resolve(__dirname, '..', 'app')
    },
    plugins: [
        new webpack.BannerPlugin({ banner: "#!/usr/bin/env node", raw: true }),
        new webpack.ContextReplacementPlugin(
            /express\/lib/,
            path.resolve('node_modules'),
            {
                'ejs': 'ejs'
            }
        )
    ],
    resolve: {
        extensions: ['.ts', '.js']
    },
    target: 'node'
};
