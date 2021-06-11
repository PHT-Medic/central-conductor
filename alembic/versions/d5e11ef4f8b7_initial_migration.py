"""initial migration

Revision ID: d5e11ef4f8b7
Revises: 
Create Date: 2021-06-11 15:07:13.304670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5e11ef4f8b7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_stations_id'), 'stations', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('hashed_password', sa.String(), nullable=True),
    sa.Column('institution', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('trains',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('proposal_id', sa.Integer(), nullable=True),
    sa.Column('creator_id', sa.Integer(), nullable=True),
    sa.Column('key', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['creator_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_trains_id'), 'trains', ['id'], unique=False)
    op.create_table('discovery_results',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('station_id', sa.Integer(), nullable=True),
    sa.Column('results', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['station_id'], ['stations.id'], ),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('train_id', 'station_id')
    )
    op.create_index(op.f('ix_discovery_results_id'), 'discovery_results', ['id'], unique=False)
    op.create_table('dl_models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('model_id', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('model_type', sa.String(), nullable=True),
    sa.Column('model_name', sa.String(), nullable=True),
    sa.Column('model_src', sa.String(), nullable=True),
    sa.Column('model_logs', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('model_id')
    )
    op.create_index(op.f('ix_dl_models_id'), 'dl_models', ['id'], unique=False)
    op.create_table('msg_advertise_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('station_id', sa.Integer(), nullable=True),
    sa.Column('iteration', sa.Integer(), nullable=True),
    sa.Column('signing_key', sa.String(), nullable=True),
    sa.Column('sharing_key', sa.String(), nullable=True),
    sa.Column('key_signature', sa.String(), nullable=True),
    sa.Column('received_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['station_id'], ['stations.id'], ),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_msg_advertise_keys_id'), 'msg_advertise_keys', ['id'], unique=False)
    op.create_table('msg_share_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('sender', sa.Integer(), nullable=True),
    sa.Column('recipient', sa.Integer(), nullable=True),
    sa.Column('cypher', sa.String(), nullable=True),
    sa.Column('iteration', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['sender'], ['stations.id'], ),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_msg_share_keys_id'), 'msg_share_keys', ['id'], unique=False)
    op.create_table('train_configs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('min_participants', sa.Integer(), nullable=True),
    sa.Column('dropout_allowance', sa.Float(), nullable=True),
    sa.Column('batch_size', sa.Integer(), nullable=True),
    sa.Column('epochs', sa.Integer(), nullable=True),
    sa.Column('time_out', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_train_configs_id'), 'train_configs', ['id'], unique=False)
    op.create_table('train_link',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('station_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['station_id'], ['stations.id'], ),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_train_link_id'), 'train_link', ['id'], unique=False)
    op.create_table('train_states',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('train_id', sa.Integer(), nullable=True),
    sa.Column('iteration', sa.Integer(), nullable=True),
    sa.Column('round', sa.Integer(), nullable=True),
    sa.Column('round_start', sa.DateTime(), nullable=True),
    sa.Column('round_k', sa.Integer(), nullable=True),
    sa.Column('round_ready', sa.Boolean(), nullable=True),
    sa.Column('round_messages_sent', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('epoch', sa.Integer(), nullable=True),
    sa.Column('discovery_finished', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['train_id'], ['trains.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_train_states_id'), 'train_states', ['id'], unique=False)
    op.create_table('model_checkpoints',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dl_model_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('checkpoint_path', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['dl_model_id'], ['dl_models.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_model_checkpoints_id'), 'model_checkpoints', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_model_checkpoints_id'), table_name='model_checkpoints')
    op.drop_table('model_checkpoints')
    op.drop_index(op.f('ix_train_states_id'), table_name='train_states')
    op.drop_table('train_states')
    op.drop_index(op.f('ix_train_link_id'), table_name='train_link')
    op.drop_table('train_link')
    op.drop_index(op.f('ix_train_configs_id'), table_name='train_configs')
    op.drop_table('train_configs')
    op.drop_index(op.f('ix_msg_share_keys_id'), table_name='msg_share_keys')
    op.drop_table('msg_share_keys')
    op.drop_index(op.f('ix_msg_advertise_keys_id'), table_name='msg_advertise_keys')
    op.drop_table('msg_advertise_keys')
    op.drop_index(op.f('ix_dl_models_id'), table_name='dl_models')
    op.drop_table('dl_models')
    op.drop_index(op.f('ix_discovery_results_id'), table_name='discovery_results')
    op.drop_table('discovery_results')
    op.drop_index(op.f('ix_trains_id'), table_name='trains')
    op.drop_table('trains')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_stations_id'), table_name='stations')
    op.drop_table('stations')
    # ### end Alembic commands ###