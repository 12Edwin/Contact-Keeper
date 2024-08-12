import Vue from "vue";
import VueRouter from "vue-router";
import privateRoutes from "@/router/private-routes";
import publicRoutes from "@/router/public-routes";
import utils from "@/kernel/utils";
Vue.use(VueRouter);

const routes = [
  {
    path: "",
    redirect: "/",
  },
  {
    path: '/',
        component: {
            render (c){
                return c("router-view")
            }
        },
        children: [
            ...privateRoutes.map((route) => {
                route.meta.requireAuth = true
                return { ...route };
            }),
            ...publicRoutes.map((route) => {
                route.meta.requireAuth = false
                return { ...route };
            }),
        ],
   },
  {
    name: "unautorized",
    path: "/unautorized",
    component: () => import("@/components/Unautorized.vue"),
  },
];

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})


router.beforeEach((to, from, next) => {
    const publicRoutes = ["/login"];
    const authRequired = !publicRoutes.includes(to.path);
    const loggedIn = utils.getToken();

    if (authRequired && !loggedIn) {
      return next("/login");
    }
    if (loggedIn) {
      const role = utils.getRoleStorage();

      if (role) {
        if (to.meta && to.meta.role && to.meta.role.toString().toLowerCase() !== role.toString().toLowerCase()) {
          return next("/unautorized");
        }
      } else {
        return next("/login");
      }
      next();
    }
    if (loggedIn && to.path.toString().toLowerCase() === "/login") {
      return next("/users");
    }
    next();
});

export default router;
