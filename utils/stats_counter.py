with open('stats.txt') as file:
    d = file.read().split('---')

do_job_on_website = 0
find_required_fields_for_input = 0
find_optional_fields_for_input = 0
solve_captcha = 0
submit_form = 0
click_back = 0
click_on_adv_banner = 0
do_random_stuff = 0
click_random_button = 0

for case in d:
    dag = case.strip().split('\n')
    dag = [i for i in dag if i]
    if 'do_job on website' in dag:
        do_job_on_website += 1
    if 'find_required_fields_for_input' in dag:
        find_required_fields_for_input += 1
    if 'find_optional_fields_for_input' in dag:
        find_optional_fields_for_input += 1
    if 'solve_captcha' in dag:
        solve_captcha += 1
    if 'submit_form' in dag:
        submit_form += 1
    if 'click_back' in dag:
        click_back += 1
    if 'click_on_adv_banner' in dag:
        click_on_adv_banner += 1
    if 'do_random_stuff' in dag:
        do_random_stuff += 1
    if 'click_random_button' in dag:
        click_random_button += 1

print(f'do_job_on_website = {round(do_job_on_website / len(d), 2)}')
print(f'find_required_fields_for_input = {round(find_required_fields_for_input / len(d), 2)}')
print(f'find_optional_fields_for_input = {round(find_optional_fields_for_input / len(d), 2)}')
print(f'solve_captcha = {round(solve_captcha / len(d), 2)}')
print(f'submit_form = {round(submit_form / len(d), 2)}')
print(f'click_back = {round(click_back / len(d), 2)}')
print(f'click_on_adv_banner = {round(click_on_adv_banner / len(d), 2)}')
print(f'do_random_stuff = {round(do_random_stuff / len(d), 2)}')
print(f'click_random_button = {round(click_random_button / len(d), 2)}')