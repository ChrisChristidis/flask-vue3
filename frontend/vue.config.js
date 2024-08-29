// vue.config.js
const { defineConfig } = require("@vue/cli-service");
const { BootstrapVueNextResolver } = require("bootstrap-vue-next");
const webpack = require("webpack");

module.exports = defineConfig({
  configureWebpack: {
    plugins: [
      new webpack.DefinePlugin({
        // Vue CLI is in maintenance mode, and probably won't merge my PR to fix this in their tooling
        // https://github.com/vuejs/vue-cli/pull/7443
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "false",
      }),
      require("unplugin-vue-components/webpack").default({
        // Automatically register components from BootstrapVueNext
        resolvers: [BootstrapVueNextResolver()],
      }),
    ],
  },
});
