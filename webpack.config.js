const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env) => {
    return {
        mode: env["production"] ? "production" : "development",
        devtool: env["production"] ? false : "eval-source-map",
        plugins: [new MiniCssExtractPlugin()],
        entry: {
            base: "./web_src/ts/base.ts",
        },
        resolve: {
            extensions: [".ts", ".js"],
        },
        output: {
            filename: "[name].js",
            path: path.resolve(__dirname, "./manim_editor/app/static/build"),
        },
        module: {
            rules: [
                // SCSS
                {
                    // inject CSS to page
                    test: /\.(scss)$/,
                    use: [
                        // {
                        //     loader: "style-loader",
                        // },
                        {
                            // bundle in separate CSS file
                            // <- loading with JavaScript takes a few millisections every time the page reloads
                            loader: MiniCssExtractPlugin.loader,
                        },
                        {
                            // translate CSS into CommonJS modules
                            loader: "css-loader",
                        },
                        // {
                        //     // run PostCSS actions
                        //     loader: "postcss-loader",
                        //     options: {
                        //         postcssOptions: {
                        //             plugins: function() {
                        //                 return [
                        //                     require("autoprefixer")
                        //                 ];
                        //             }
                        //         }
                        //     },
                        // },
                        {
                            // compile SCSS to Css
                            loader: "sass-loader",
                        }
                    ]
                },
                // TypeScript
                {
                    test: /\.ts$/,
                    use: "ts-loader",
                    include: [path.resolve(__dirname, "src")],
                }
            ]
        }
    };
};
