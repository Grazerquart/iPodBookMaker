import os
import sys
name = sys.argv[1]
input_file = sys.argv[2]

def split_book_at_newlines(input_file, name, max_chunk_size_kb=4, target_chunk_size_kb=3.7):
    # Convert sizes from KB to bytes
    max_chunk_size = max_chunk_size_kb * 1024
    target_chunk_size = target_chunk_size_kb * 1024

    # Read the entire book into a list of lines
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_chunk = []
    current_chunk_size = 0
    chunk_number = 1

    # Helper function to write the current chunk to a file
    def write_chunk(chunk_number, lines, name):
        if not os.path.isdir(f'.\\{name}'):
            os.mkdir(f'.\\{name}')
        chunk_filename = f'.\\{name}\\{name}_{chunk_number}'
        with open(chunk_filename, 'w', encoding='utf-8') as chunk_file:
            chunk_file.writelines(lines)
        print(f'Saved {chunk_filename}')
    def write_title_page(name, chunk_number):
        title_page_filename = f'.\\{name}_book_entry_page'
        with open(title_page_filename, 'w', encoding='utf-8') as title_page_file:
            title_page_file.writelines(f'<title>{name}</title><a href=\"{name}/{name}_1\">First</a>')
        print(f'Saved {title_page_filename}')

    # Process lines to create chunks
    for line in lines:
        line_size = len(line.encode('utf-8'))
        
        # Check if adding this line exceeds the target chunk size
        if current_chunk_size + line_size > target_chunk_size:
            # If the current chunk size exceeds the target, but is within max_chunk_size, write it
            if current_chunk_size + line_size <= max_chunk_size:
                current_chunk.append(line)
                current_chunk_size += line_size
                current_chunk.append(f'<a href=\"{name}_{chunk_number + 1}\">Next</a><title>{name}-{chunk_number}</title>')
            # Write the current chunk to a file
            write_chunk(chunk_number, current_chunk, name)
            # Reset for the next chunk
            current_chunk = []
            current_chunk_size = 0
            chunk_number += 1
            
            # Add the current line to the new chunk
            current_chunk.append(line)
            current_chunk_size += line_size
        else:
            # Accumulate lines
            current_chunk.append(line)
            current_chunk_size += line_size

    # Write the last chunk if it has any content
    if current_chunk:
        write_chunk(chunk_number, current_chunk, name)
        #write_title_page(name, chunk_number)


# Example usage
split_book_at_newlines(input_file, name)
