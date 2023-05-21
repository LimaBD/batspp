#!/usr/bin/env bats
#
# This test file was generated using Batspp
# https://github.com/LimaBD/batspp
#

# Constants
VERBOSE_DEBUG="| hexdump -C"
TEMP_DIR="/tmp/batspp-32737"

# Setup function
# $1 -> test name
function run_setup () {
	test_folder=$(echo $TEMP_DIR/$1-$$)
	mkdir --parents "$test_folder"
	cd "$test_folder" || echo Warning: Unable to "cd $test_folder"
}

# Teardown function
function run_teardown () {
	: # Nothing here...
}

@test "test of line 1" {
	run_setup "test-of-line-1"

	# Assertion of line 1
	shopt -s expand_aliases
	print_debug "$(echo -e "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor a libero nec sagittis. Nunc est nibh, molestie vel cursus id, venenatis ut dui. Donec rutrum at mi aliquam molestie. Maecenas nec condimentum augue. Sed nec rhoncus diam. Vestibulum sit amet convallis libero, nec cursus dui. Fusce augue nisi, tempus et elit suscipit, luctus vehicula tortor. Maecenas aliquet eu justo vitae consequat.\n\nNullam porta laoreet consequat. Donec quam lorem, porta non turpis vel, consectetur pellentesque tortor. Aliquam at eros nec nibh mattis euismod. Quisque scelerisque sem mi, at porta ligula finibus nec. Nulla congue velit vel nisi porttitor laoreet. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam at tempor odio. Nulla in accumsan leo. Nam vitae sapien vitae turpis dictum pulvinar. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam id eros vel velit convallis ornare. In venenatis feugiat sagittis. Aliquam id lacus id urna interdum varius. Praesent eget neque blandit, pharetra sapien quis, semper mi.\n\n\nDonec eget nibh enim. Quisque gravida purus vel augue viverra, sit amet convallis sem gravida. Donec quis consequat purus. Aliquam nec commodo lacus, ut auctor tellus. Praesent vel elementum nunc. Nulla at risus ac magna aliquam lobortis eget ac nibh. Aliquam erat volutpat. Duis in dolor vitae tellus scelerisque semper a id odio. Vivamus sodales lacus odio, id tristique velit bibendum a. Sed ex felis, tristique vitae auctor in, maximus tempus tellus.\n\n\n\nVivamus blandit quam risus, eu faucibus felis elementum ultricies. Nunc vitae neque quis quam aliquet imperdiet. Morbi id fringilla nunc. Donec quis nulla vel nibh porttitor consectetur blandit ut velit. Aliquam ut velit nibh. Ut laoreet, massa sed pharetra placerat, ipsum erat pellentesque velit, eget scelerisque tellus turpis a nibh. Phasellus porttitor eleifend felis ac aliquet. Fusce pharetra mollis enim, et ornare augue porttitor sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam feugiat faucibus fermentum. Nulla finibus nec libero in pellentesque. Fusce egestas leo eu viverra convallis. In in orci vitae lorem placerat vehicula. Praesent pellentesque velit id enim auctor, at feugiat felis consectetur.\n\nPellentesque efficitur purus id convallis dapibus. Etiam eu nibh id justo bibendum sollicitudin. Morbi at purus purus. Nunc in ex sed augue eleifend laoreet porta sed ipsum. Fusce pharetra tincidunt nunc vel sagittis. Nulla facilisi. Proin at elit nisl. Mauris et commodo ligula. In vitae condimentum magna, in finibus erat. Aenean elementum quis enim id cursus. Aliquam ac porttitor nisi. Quisque id lacus dolor. Sed suscipit sapien in interdum ullamcorper. Cras lorem nunc, fringilla vel lacus ut, pellentesque commodo odio. Vestibulum sit amet odio mattis, sollicitudin dolor ut, blandit libero. Fusce id nisi ligula.\n")" "$(echo -e 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor a libero nec sagittis. Nunc est nibh, molestie vel cursus id, venenatis ut dui. Donec rutrum at mi aliquam molestie. Maecenas nec condimentum augue. Sed nec rhoncus diam. Vestibulum sit amet convallis libero, nec cursus dui. Fusce augue nisi, tempus et elit suscipit, luctus vehicula tortor. Maecenas aliquet eu justo vitae consequat.\n\nNullam porta laoreet consequat. Donec quam lorem, porta non turpis vel, consectetur pellentesque tortor. Aliquam at eros nec nibh mattis euismod. Quisque scelerisque sem mi, at porta ligula finibus nec. Nulla congue velit vel nisi porttitor laoreet. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam at tempor odio. Nulla in accumsan leo. Nam vitae sapien vitae turpis dictum pulvinar. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam id eros vel velit convallis ornare. In venenatis feugiat sagittis. Aliquam id lacus id urna interdum varius. Praesent eget neque blandit, pharetra sapien quis, semper mi.\n\n\nDonec eget nibh enim. Quisque gravida purus vel augue viverra, sit amet convallis sem gravida. Donec quis consequat purus. Aliquam nec commodo lacus, ut auctor tellus. Praesent vel elementum nunc. Nulla at risus ac magna aliquam lobortis eget ac nibh. Aliquam erat volutpat. Duis in dolor vitae tellus scelerisque semper a id odio. Vivamus sodales lacus odio, id tristique velit bibendum a. Sed ex felis, tristique vitae auctor in, maximus tempus tellus.\n\n\n\nVivamus blandit quam risus, eu faucibus felis elementum ultricies. Nunc vitae neque quis quam aliquet imperdiet. Morbi id fringilla nunc. Donec quis nulla vel nibh porttitor consectetur blandit ut velit. Aliquam ut velit nibh. Ut laoreet, massa sed pharetra placerat, ipsum erat pellentesque velit, eget scelerisque tellus turpis a nibh. Phasellus porttitor eleifend felis ac aliquet. Fusce pharetra mollis enim, et ornare augue porttitor sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam feugiat faucibus fermentum. Nulla finibus nec libero in pellentesque. Fusce egestas leo eu viverra convallis. In in orci vitae lorem placerat vehicula. Praesent pellentesque velit id enim auctor, at feugiat felis consectetur.\n\nPellentesque efficitur purus id convallis dapibus. Etiam eu nibh id justo bibendum sollicitudin. Morbi at purus purus. Nunc in ex sed augue eleifend laoreet porta sed ipsum. Fusce pharetra tincidunt nunc vel sagittis. Nulla facilisi. Proin at elit nisl. Mauris et commodo ligula. In vitae condimentum magna, in finibus erat. Aenean elementum quis enim id cursus. Aliquam ac porttitor nisi. Quisque id lacus dolor. Sed suscipit sapien in interdum ullamcorper. Cras lorem nunc, fringilla vel lacus ut, pellentesque commodo odio. Vestibulum sit amet odio mattis, sollicitudin dolor ut, blandit libero. Fusce id nisi ligula.\n')"
	[ "$(echo -e "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor a libero nec sagittis. Nunc est nibh, molestie vel cursus id, venenatis ut dui. Donec rutrum at mi aliquam molestie. Maecenas nec condimentum augue. Sed nec rhoncus diam. Vestibulum sit amet convallis libero, nec cursus dui. Fusce augue nisi, tempus et elit suscipit, luctus vehicula tortor. Maecenas aliquet eu justo vitae consequat.\n\nNullam porta laoreet consequat. Donec quam lorem, porta non turpis vel, consectetur pellentesque tortor. Aliquam at eros nec nibh mattis euismod. Quisque scelerisque sem mi, at porta ligula finibus nec. Nulla congue velit vel nisi porttitor laoreet. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam at tempor odio. Nulla in accumsan leo. Nam vitae sapien vitae turpis dictum pulvinar. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam id eros vel velit convallis ornare. In venenatis feugiat sagittis. Aliquam id lacus id urna interdum varius. Praesent eget neque blandit, pharetra sapien quis, semper mi.\n\n\nDonec eget nibh enim. Quisque gravida purus vel augue viverra, sit amet convallis sem gravida. Donec quis consequat purus. Aliquam nec commodo lacus, ut auctor tellus. Praesent vel elementum nunc. Nulla at risus ac magna aliquam lobortis eget ac nibh. Aliquam erat volutpat. Duis in dolor vitae tellus scelerisque semper a id odio. Vivamus sodales lacus odio, id tristique velit bibendum a. Sed ex felis, tristique vitae auctor in, maximus tempus tellus.\n\n\n\nVivamus blandit quam risus, eu faucibus felis elementum ultricies. Nunc vitae neque quis quam aliquet imperdiet. Morbi id fringilla nunc. Donec quis nulla vel nibh porttitor consectetur blandit ut velit. Aliquam ut velit nibh. Ut laoreet, massa sed pharetra placerat, ipsum erat pellentesque velit, eget scelerisque tellus turpis a nibh. Phasellus porttitor eleifend felis ac aliquet. Fusce pharetra mollis enim, et ornare augue porttitor sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam feugiat faucibus fermentum. Nulla finibus nec libero in pellentesque. Fusce egestas leo eu viverra convallis. In in orci vitae lorem placerat vehicula. Praesent pellentesque velit id enim auctor, at feugiat felis consectetur.\n\nPellentesque efficitur purus id convallis dapibus. Etiam eu nibh id justo bibendum sollicitudin. Morbi at purus purus. Nunc in ex sed augue eleifend laoreet porta sed ipsum. Fusce pharetra tincidunt nunc vel sagittis. Nulla facilisi. Proin at elit nisl. Mauris et commodo ligula. In vitae condimentum magna, in finibus erat. Aenean elementum quis enim id cursus. Aliquam ac porttitor nisi. Quisque id lacus dolor. Sed suscipit sapien in interdum ullamcorper. Cras lorem nunc, fringilla vel lacus ut, pellentesque commodo odio. Vestibulum sit amet odio mattis, sollicitudin dolor ut, blandit libero. Fusce id nisi ligula.\n")" == "$(echo -e 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras tempor a libero nec sagittis. Nunc est nibh, molestie vel cursus id, venenatis ut dui. Donec rutrum at mi aliquam molestie. Maecenas nec condimentum augue. Sed nec rhoncus diam. Vestibulum sit amet convallis libero, nec cursus dui. Fusce augue nisi, tempus et elit suscipit, luctus vehicula tortor. Maecenas aliquet eu justo vitae consequat.\n\nNullam porta laoreet consequat. Donec quam lorem, porta non turpis vel, consectetur pellentesque tortor. Aliquam at eros nec nibh mattis euismod. Quisque scelerisque sem mi, at porta ligula finibus nec. Nulla congue velit vel nisi porttitor laoreet. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Nam at tempor odio. Nulla in accumsan leo. Nam vitae sapien vitae turpis dictum pulvinar. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aliquam id eros vel velit convallis ornare. In venenatis feugiat sagittis. Aliquam id lacus id urna interdum varius. Praesent eget neque blandit, pharetra sapien quis, semper mi.\n\n\nDonec eget nibh enim. Quisque gravida purus vel augue viverra, sit amet convallis sem gravida. Donec quis consequat purus. Aliquam nec commodo lacus, ut auctor tellus. Praesent vel elementum nunc. Nulla at risus ac magna aliquam lobortis eget ac nibh. Aliquam erat volutpat. Duis in dolor vitae tellus scelerisque semper a id odio. Vivamus sodales lacus odio, id tristique velit bibendum a. Sed ex felis, tristique vitae auctor in, maximus tempus tellus.\n\n\n\nVivamus blandit quam risus, eu faucibus felis elementum ultricies. Nunc vitae neque quis quam aliquet imperdiet. Morbi id fringilla nunc. Donec quis nulla vel nibh porttitor consectetur blandit ut velit. Aliquam ut velit nibh. Ut laoreet, massa sed pharetra placerat, ipsum erat pellentesque velit, eget scelerisque tellus turpis a nibh. Phasellus porttitor eleifend felis ac aliquet. Fusce pharetra mollis enim, et ornare augue porttitor sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Aliquam feugiat faucibus fermentum. Nulla finibus nec libero in pellentesque. Fusce egestas leo eu viverra convallis. In in orci vitae lorem placerat vehicula. Praesent pellentesque velit id enim auctor, at feugiat felis consectetur.\n\nPellentesque efficitur purus id convallis dapibus. Etiam eu nibh id justo bibendum sollicitudin. Morbi at purus purus. Nunc in ex sed augue eleifend laoreet porta sed ipsum. Fusce pharetra tincidunt nunc vel sagittis. Nulla facilisi. Proin at elit nisl. Mauris et commodo ligula. In vitae condimentum magna, in finibus erat. Aenean elementum quis enim id cursus. Aliquam ac porttitor nisi. Quisque id lacus dolor. Sed suscipit sapien in interdum ullamcorper. Cras lorem nunc, fringilla vel lacus ut, pellentesque commodo odio. Vestibulum sit amet odio mattis, sollicitudin dolor ut, blandit libero. Fusce id nisi ligula.\n')" ]

	run_teardown
}

# This prints debug data when an assertion fail
# $1 -> actual value
# $2 -> expected value
function print_debug() {
	echo "=======  actual  ======="
	bash -c "echo \"$1\" $VERBOSE_DEBUG"
	echo "======= expected ======="
	bash -c "echo \"$2\" $VERBOSE_DEBUG"
	echo "========================"
}