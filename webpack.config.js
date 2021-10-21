const path = require("path");

module.exports = (env) => {
    return {
        mode: env["production"] ? "production" : "development",
        devtool: env["production"] ? false : "eval-source-map",
        entry: {
            index: "./web_src/ts/index.ts",
        },
        resolve: {
            extensions: [".ts", ".js"],
        },
        output: {
            filename: "[name].js",
            path: path.resolve(__dirname, "./manim_editor/app/static/js"),
        },
        module: {
            rules: [{
                // SCSS
                // inject CSS to page
                test: /\.(scss)$/,
                use: [{
                    loader: "style-loader",
                }, {
                    // translate CSS into CommonJS modules
                    loader: "css-loader",
                }, {
                    // run PostCSS actions
                    loader: "postcss-loader",
                    options: {
                        postcssOptions: {
                            plugins: function() {
                                return [
                                    require("autoprefixer")
                                ];
                            }
                        }
                    },
                }, {
                    // compile SCSS to Css
                    loader: "sass-loader",
                }]
            }, {
                // TypeScript
                test: /\.ts$/,
                use: "ts-loader",
                include: [path.resolve(__dirname, "src")],
            },],
        },
    };
};
