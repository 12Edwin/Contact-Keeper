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
    path: "/",
    component: {
      render(c) {
        return c("router-view");
      },
    },
    children: [
      ...privateRoutes.map((route) => {
        route.meta.requireAuth = true;
        return { ...route };
      }),
      ...publicRoutes.map((route) => {
        route.meta.requireAuth = false;
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
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

router.beforeEach(async (to, from, next) => {
  try {
    console.log("TO: ", to);
    console.log("FROM: ", from);
    
    const publicRoutes = ["/login", "/signup"];
    const authRequired = !publicRoutes.includes(to.path);
    const loggedIn = utils.getToken();

    if (authRequired && !loggedIn) {
      return next("/login");
    }
    if (loggedIn) {
      const role = utils.getRoleStorage();
      console.log(role);

      if (
        role.toLowerCase() !== "administrators" &&
        role.toLowerCase() !== "normalusers" &&
        role !== undefined &&
        role !== null &&
        role !== ""
      ) {
        console.log("entro al if :)");

        if (
          to.meta &&
          to.meta.role &&
          to.meta.role.toString().toLowerCase() !==
            role.toString().toLowerCase()
        ) {
          return next("/unautorized");
        }
      } else {
        return next("/login");
      }
      next();
    }
    if (loggedIn && to.path.toString().toLowerCase() === "/login") {
      console.log("entro a redirigir XD");

      return next("/users");
    }
    next();
  } catch (error) {
    console.log("ERROR: ", error);
  }
});

export default router;
