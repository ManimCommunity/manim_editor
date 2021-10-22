const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = (env) => {
    return {
        mode: env["production"] ? "production" : "development",
        devtool: env["production"] ? false : "eval-source-map",
        plugins: [new MiniCssExtractPlugin()],
        entry: {
            base: "./web_src/ts/base.ts",
            section_selection: "./web_src/ts/section_selection.ts",
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
                        {
                            // bundle in separate CSS file
                            // <- loading with JavaScript takes a few millisections every time the page reloads
                            loader: MiniCssExtractPlugin.loader,
                        },
                        {
                            // translate CSS into CommonJS modules
                            loader: "css-loader",
                        },
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
                    include: [
                        path.resolve(__dirname, "./web_src/ts"),
                        path.resolve(__dirname, "./web_src/scss"),
                    ],
                }
            ]
        }
    };
};
