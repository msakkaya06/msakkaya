using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace DataAccess.Migrations
{
    /// <inheritdoc />
    public partial class ActvityTableUpdate : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_LifeCoachMaster_ActivityId",
                table: "LifeCoachMaster");

            migrationBuilder.RenameColumn(
                name: "Active",
                table: "Activities",
                newName: "isActive");

            migrationBuilder.AlterColumn<int>(
                name: "CodeEnvironment",
                table: "Activities",
                type: "int",
                nullable: true,
                oldClrType: typeof(int),
                oldType: "int");

            migrationBuilder.CreateIndex(
                name: "IX_LifeCoachMaster_ActivityId",
                table: "LifeCoachMaster",
                column: "ActivityId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropIndex(
                name: "IX_LifeCoachMaster_ActivityId",
                table: "LifeCoachMaster");

            migrationBuilder.RenameColumn(
                name: "isActive",
                table: "Activities",
                newName: "Active");

            migrationBuilder.AlterColumn<int>(
                name: "CodeEnvironment",
                table: "Activities",
                type: "int",
                nullable: false,
                defaultValue: 0,
                oldClrType: typeof(int),
                oldType: "int",
                oldNullable: true);

            migrationBuilder.CreateIndex(
                name: "IX_LifeCoachMaster_ActivityId",
                table: "LifeCoachMaster",
                column: "ActivityId",
                unique: true);
        }
    }
}
