<template>
  <div id="rovu-nav navbar navbar-default">
    <div class="container-fluid">
      <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
        <ul class="nav navbar-nav">
          <li class="active"><a href="javascript:void(0)">Link <span class="sr-only">(current)</span></a></li>
          <li><a href="javascript:void(0)">Link</a></li>
          <li class="dropdown">
            <a href="javascript:void(0)" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">Show Events<span class="caret"></span></a>
            <ul class="dropdown-menu">
              <li><a href="javascript:void(0)">Within 24hrs</a></li>
              <li><a href="javascript:void(0)">In the next 3 days</a></li>
              <li><a href="javascript:void(0)">In up to 7 days</a></li>
              <li role="separator" class="divider"></li>
              <li><a href="javascript:void(0)">This weekend</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>


<style>
</style>


<script>
export default {
  name: 'rovu-nav',
};
</script>
