<!-- <template>
  <v-sheet
    :color="`grey ${theme.isDark ? 'darken-2' : 'lighten-4'}`"
    class="pa-3"
  >
    <v-skeleton-loader
      class="mx-auto"
      max-width="300"
      type="card"
    ></v-skeleton-loader>
  </v-sheet>
</template>

<script>
  export default {
    // Vuetify components provide
    // a theme variable that is
    // used to determine dark
    inject: {
      theme: {
        default: { isDark: false },
      },
    },
  }
</script> -->

<template>
  <v-card flat tile>
    <v-toolbar color="blue" dark>
  
      <v-toolbar-title>CANDIDATOS</v-toolbar-title>

      <v-spacer></v-spacer>

    </v-toolbar>

    <v-container v-for="type in types" :key="type" class="grey lighten-4" fluid>
    
      <v-row>
        <v-spacer></v-spacer>
        <v-col v-for="card in cards" :key="card" cols="12" sm="6" md="4">
          <v-card>

            <!-- <v-btn> -->
                <v-img :src="`https://picsum.photos/200/300?image=${getImage()}`" height="300px">
                    <span class="text-h5 white--text pl-4 pt-4 d-inline-block" v-text="card"></span>
                </v-img>
            <!-- </v-btn> -->

            <v-card-actions class="white justify-center">
              <!-- <v-btn v-for="(social, i) in socials" :key="i" :color="social.color" class="white--text" fab icon small>
                <v-icon>{{ social.icon }}</v-icon>
              </v-btn> -->
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
  export default {
    data: () => ({
      types: ['Candidatos'],
      cards: ['1er Candidato', '2do Candidato', '3er Candidato'],
      socials: [
        {
          icon: 'mdi-facebook',
          color: 'indigo',
        },
        {
          icon: 'mdi-linkedin',
          color: 'cyan darken-1',
        },
        {
          icon: 'mdi-instagram',
          color: 'red lighten-3',
        },
      ],
    }),

    methods: {
      getImage () {
        const min = 550
        const max = 560

        return Math.floor(Math.random() * (max - min + 1)) + min
      },
    },
  }
</script>