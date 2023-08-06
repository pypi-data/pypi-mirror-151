import click


def delete_term_n_previous_line(n):
    for i in range(n):
        click.get_text_stream('stdout').write('\033[A\r\033[K')
