import Profile from "@/modules/users/views/Profile.vue";
export default [
  {
    path: "profile",
    name: "profile",
    meta: {
      role: "NormalUsers",
    },
    component: {
      render(c) {
        return c("router-view");
      },
    },
    children: [
      {
        path: '',
        name: 'profile',
        component: Profile,
        meta: {
          title: "Perfil",
          role: 'NormalUsers'
        },
      },
    ]
  },
];
