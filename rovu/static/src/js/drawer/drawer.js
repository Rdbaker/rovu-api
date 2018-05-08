import { mapActions, mapGetters } from 'vuex';
import Datepicker from 'vuejs-datepicker';
import { merge } from 'lodash';


export default {
  name: 'rovu-drawer',

  components: {
    Datepicker,
  },

  computed: mapGetters({
    isActive: 'mobileSearchDrawerOpen',
    startDate: 'searchEventStart',
    endDate: 'searchEventEnd',
  }),

  methods: merge(
    mapActions(['closeMobileSearchDrawer']),
    {
      setStartDate: function(date) {
        this.$store.dispatch('setSearchStart', !!date ? date.toISOString() : date)
        this.$store.dispatch('fetchEvents')
      }
    }
  ),
}