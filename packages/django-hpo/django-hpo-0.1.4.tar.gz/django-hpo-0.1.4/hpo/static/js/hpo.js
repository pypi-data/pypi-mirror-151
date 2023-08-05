/*
* .replace('//', '/') serve per diverse configurazioni nel settings di force_script_name
* */
function setAutocomplete($el) {
  $(document).on('keydown.autocomplete', $el, function() {
    $(this).autocomplete({
      source: `${force_script_name}/hpo/phenotype/`.replace('//', '/'),
      select: autoCompleteSelectHandlerPhenotype,
      minLength: 3,
      sdelay: 300
    });
    $el.each(function( index ) {
    $(this).autocomplete("instance")._renderItem = function (ul, item) {
      return $("<li>")
        .append("<div>" + item.label + (item.phenotypes !== undefined ? '<br>' + item.phenotypes : '') + (item.titles !== undefined ? '<br>' + item.titles : '') + "</div>")
        .appendTo(ul);
    };
  });
});

}

$('button.add').click(function (event) {
  event.preventDefault();
  let clone = $("#row_model").clone(true).attr('id', '').removeClass("hidden").addClass("row");
  $(".rows").append(clone);
  console.log(clone.find('input[hpo=phenotype]'));
  //setAutocomplete($(clone.find('input[hpo=phenotype]')));
});

function autoCompleteSelectHandlerPhenotype(event, ui) {
  $(`#${ event.target.attributes['id'].value.slice(0, -13) }_id`).val(ui.item.id);
  let notes = $(event.target).closest(".row").find(`.notes`);
  notes.html(`<span class="help-block"><a target="_blank" href="https://hpo.jax.org/app/browse/term/${ui.item.id}">More info on HPO's page.</a></span>`);
}


//setAutocomplete($('input[hpo=phenotype]'));

$(document).on('keydown.autocomplete', 'input[hpo=phenotype]', function() {
  $(this).autocomplete({
    source: `${force_script_name}/hpo/phenotype/`.replace('//', '/'),
    select: autoCompleteSelectHandlerPhenotype,
    minLength: 3,
    sdelay: 300
  });
  $(this).each(function (index) {
    $(this).autocomplete("instance")._renderItem = function (ul, item) {
      return $("<li>")
          .append("<div>" + item.label + (item.phenotypes !== undefined ? '<br>' + item.phenotypes : '') + (item.titles !== undefined ? '<br>' + item.titles : '') + "</div>")
          .appendTo(ul);
    };
  });
});



var phenotypeRenderItem = function(event, ui) {
  $(event.target).val(ui.item.id);
  $(event.target).closest(".row").append(`<p class="notes"><span class="help-block"><a target="_blank" href="https://hpo.jax.org/app/browse/term/${ui.item.id}">More info on HPO's page.</a></span></p>`);
}
