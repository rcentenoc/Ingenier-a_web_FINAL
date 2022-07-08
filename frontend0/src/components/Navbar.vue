<template>
    <nav>
        <v-app-bar color="black" dark app>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer">
            
            </v-app-bar-nav-icon>
            <v-toolbar-title app  class="text-uppercase">

                <v-btn text>
                    <span>VOTO</span>
                    <v-icon right>
                    thumb_up
                    </v-icon>
                </v-btn>

            </v-toolbar-title>

            <v-spacer></v-spacer>
            
            <v-menu offset-y>
                <template v-slot:activator="{on}">
                    <v-btn text v-on="on">
                        <v-icon left>
                            expand_more
                        </v-icon>
                        <span>Menu</span>
                    </v-btn>
                </template>
                <v-list flat>
                    <v-list-item v-for="link in links" :key="link.text" router :to="link.route" active-class="border">
                        <v-list-item-title>{{link.text}}</v-list-item-title>
                    </v-list-item>
                </v-list>
                
            </v-menu>

            <v-btn text>
                <span>Exit</span>
                <v-icon right>
                    exit_to_app
                </v-icon>
            </v-btn>


        </v-app-bar>
        <v-navigation-drawer v-model="drawer" dark app class="gray darken-4">
            <v-layout column align-center>
                <v-flex class="mt-5">
                    <v-avatar size="200">
                        <v-img src="/img1.png">
                        </v-img>
                    </v-avatar>
                    <p class="white--text subheading mt-1 text-center">Admin</p>
                </v-flex>
                <v-flex class="mt-4 mb-4">
                    <Popup/>
                </v-flex>
            </v-layout>
            <v-list flat>
                <v-list-item v-for="link in links" :key="link.text" router :to="link.route" active-class="border">
                    <v-list-item-action>
                        <v-icon>{{link.icon}}</v-icon>
                    </v-list-item-action>
                    <v-list-item-content>
                        <v-list-item-title>{{link.text}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list>
        </v-navigation-drawer>

    </nav>
</template>
<script>
    import Popup from './Popup.vue'
    
    export default{
        data:() => ({
            drawer: true,
            links: [
                {icon:'folder', text:'Electores', route:'/electores'},
                {icon:'person', text:'Candidatos', route:'/candidatos'},
                {icon:'chrome_reader_mode', text:'Cedulas', route:'/cedulas'},
                {icon:'maps_home_work', text:'Partidos', route:'/partidos'},
                {icon:'reduce_capacity', text:'Elecciones', route:'/elecciones'},
                {icon:'travel_explore', text:'Ubigeo', route:'/ubigeo'},
                {icon:'label_important', text:'Herramientas', route:'/'},
                {icon:'receipt', text:'Voto' , route:'/voto'},

            ],
        }),
        components: {
            Popup,
        }
    }
</script>
<style scoped>
    .border{
        border-left: 4px solid #0094ff;
    }
</style>